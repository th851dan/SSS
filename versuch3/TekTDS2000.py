# -*- coding: utf-8 -*-
"""
Wrapper class for accessing Tektronix TDS 2000 series oszilloscopes via visa interface.

@author: Martin Miller
@email: martin.miller@htwg-konstanz.de
"""

import visa as v
import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
from enum import Enum


class Singleton(type):
    """
    Singleton class for ensureing existance of only one instance of TekTDS2000.
    
    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FftType(Enum):
    SINGLE_SIDED = 1
    BOTH_SIDED = 2
    BW_200MHZ = 3
    BW_20MHZ = 4
    
class TekTDS2000(object, metaclass=Singleton):
    """
    Wrapper class for accessing Tektronix TDS 2000 series oszilloscopes via visa interface.
    
    Examples:
        >>> from TekTDS2000 import *
        >>> scope = TekTDS2000()
        >>> scope.getData(1) # returns channel 1 data

    """

    _scope = {}
    _rm = {}

    def __init__(self):
        """
        Constructor initializes an single instance.
        
        """
        self._rm = v.ResourceManager()
        devLst = self._rm.list_resources()
        self._scope = None
        for dev in devLst:
            # open visa device
            try:
                self._scope=self._rm.open_resource(dev)
            except v.VisaIOError:
                self._scope = None
                continue
            self._scope.timeout = 10000
            
            # ask for device identification 
            devIdn=''
            try:
                devIdn = self._scope.ask('*IDN?')
            except v.VisaIOError:
                self._scope.write('*RST')
                self._scope.close()
                self._scope = None
                continue
            
            # check if device is TDS 2022 oscilloscope
            if "TDS 2022" in devIdn: 
                # Tektronix TDS 2022 oscilloscope found - break
                break
        
        if self._scope is None:
            print("TekTDS2000: ERROR! Oscilloscope not found!")
            self._rm.close()
            return 
        self._scope.timeout = 15000
        return
    
    
    # destructor
    def __del__(self):
        """
        Destructor frees all used resources.

        """
        self.close()
        return
        
        
    def close(self):
        """
        Function *close()* frees all used resources.
        
        """
        self._scope.close()
        self._rm.close()
        return
        
        
    def _visaWrite(self, str):
        """
        Function *_visaWrite()* handles visa write command.
        
        """
        try:
            self._scope.write(str)
        except v.VisaIOError as e:
            print("TekTDS2000: VisaIOError({0}) -> {1}".format(e.error_code, e.description))
            return False
        return True
    
    
    def _visaAsk(self, str):
        """
        Function *_visaAsk()* handles visa ask command.
        
        """
        ret=''
        try:
            ret = self._scope.ask(str)
        except v.VisaIOError as e:
            print("TekTDS2000: VisaIOError({0}) -> {1}".format(e.error_code, e.description))
            return ret
        return ret
    
    
    def _setParam(self, ch, strt, end):
        """
        Function *_setParam()* sets transmission parameters.
        INTERNALLY USE ONLY!
        
        """
        self._visaWrite("DATa:SOUrce CH"+np.str(ch)) #choose which Channel to get
        self._visaWrite("DATa:ENCdg ASCIi") #can be ASCIi/RIBinary/RPBinary/SRIbinary/SRPbinary
        self._visaWrite("DATa:WIDth 2") #1 byte give vertical range of -128 to 127 and 2 bytes gives range of -32768 to 32767
        self._visaWrite("DATa:STARt "+np.str(strt)) #1 is far left edge
        self._visaWrite("DATa:STOP "+np.str(end)) #10,000 is far right edge
        return
    
    
    def _getData(self,strt,end):
        """
        Function *_getData()* returns sampling data. 
        INTERNALLY USE ONLY!
        
        Args:
            strt (int): start sample 
            
            end (int): end sample 
        
        Returns:
            dataX (float array): sampled x values
            
            dataY (float array): sampled y values
        
        """
        tmp=self._visaAsk("WFMPre:XINcr?")
        if tmp=='':
            return [None], [None]
        Xscaling = float(tmp) #scaling factor for the x axis
        tmp=self._visaAsk("WFMPre:YMUlt?")
        if tmp=='':
            return [None], [None]
        Yscaling = float(tmp) #scaling factor for the y axis
        tmp=self._visaAsk("WFMPre:XZEro?")
        if tmp=='':
            return [None], [None]
        Xzero = float(tmp)    #position in x units that the first sample is at
        tmp=self._visaAsk("WFMPre:YOFf?")
        if tmp=='':
            return [None], [None]
        Yoffset = float(tmp)   # vertical offset for the y axis
        raw = self._scope.ask("CURVe?")
        if raw=='':
            return [None], [None]
        data=np.array([float(s) for s in raw.split(',')])
        dataY=(data-Yoffset)*Yscaling
        #create x data range in values and not indexes
        dataX=np.arange((strt*Xscaling)+Xzero,((end+1)*Xscaling)+Xzero,Xscaling)
        return dataX,dataY
        
        
    def _chkOsciAquiParams(self, ch=1, strt=1, end=2500):
        """
        Function *_chkOsciAquiParams()* checks function parameters used by oscilloscope functions.
        INTERNALLY USE ONLY!
        
        Args:
            ch (int): channel number
            
            strt (int): start sample 
            
            end (int): end sample
        
        """
        self._chkOsciChParam(ch)
        assert type(strt) is type(1), "TekTDS2000: start sample parameter strt is not an integer: %r" % strt
        assert (strt > 0) and (strt <= 2500), "TekTDS2000: wrong start sample parameter strt: %r" % strt
        assert type(end) is type(1), "TekTDS2000: end sample parameter end is not an integer: %r" % end
        assert (end > 0) and (end <= 2500), "TekTDS2000: wrong end sample parameter end: %r" % end
        return
        
        
    def _chkOsciChParam(self, ch=1):
        """
        Function *_chkOsciChParam()* checks channel parameter *ch* used by oscilloscope functions.
        INTERNALLY USE ONLY!
        
        Args:
            ch (int): channel number
        
        """
        assert type(ch) is type(1), "TekTDS2000: channel parameter ch is not an integer: %r" % ch  
        assert (ch == 1) or (ch == 2), "TekTDS2000: wrong channel parameter ch: %r" % ch
        return
        
    
    def _chkPlotParams(self, filename, figsize, dpi):
        """
        Function *_chkPlotParams()* checks function parameters used by plot functions.
        INTERNALLY USE ONLY!
        
        Args:
            filename (String): string of filename with file extension 
            
            figsize (tuple of int): width, height in pixels
            
            dpi (int): resolution of the figure 
        
        """
        assert type(filename) is type(''), "TekTDS2000: filename string is not an string: %r" % filename
        assert type(figsize) is type((1,2)), "TekTDS2000: figsize is not an tuple: %r" % figsize
        assert type(figsize[0]) is type(1), "TekTDS2000: figsize tuple 0 is not an integer: %r" % figsize[0]
        assert type(figsize[1]) is type(1), "TekTDS2000: figsize tuple 1 is not an integer: %r" % figsize[1]
        assert type(dpi) is type(1), "TekTDS2000: dpi parameter dpi is not an integer: %r" % dpi
        return
        
        
    def getData(self, ch=1, strt=1, end=2500):
        """
        Function *getData()* returns sampling data of channel *ch*.
        
        Args:
            ch (int): channel number(s) (default: 1)
            
            strt (int): start sample (default: 1)
            
            end (int): end sample (default: 2500)
            
        Returns:
            x (float array): sampled x values of channel *ch*
            
            y (float array): sampled y values of channel *ch*
        
        """
        self._chkOsciAquiParams(ch, strt, end)
        self._setParam(ch, strt, end)
        x,y=self._getData(strt,end)
        return x,y
        
        
    def getMin(self, ch=1, verbose=True):
        """
        Function *getMin()* returns min value of channel *ch*.
        
        Args:
            ch (int): channel number (default: 1)
            
            verbose (bool): prints min value if set (default: True)
            
        Returns:
            (float): min value of channel *ch*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe MINImum')
        mini = self._visaAsk('MEASUrement:IMMed:VALue?')
        mini = float(mini)
        miniUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' min value: '+str(mini)+' '+miniUnit[1:-2])
        return mini
        
        
    def getMax(self, ch=1, verbose=True):
        """
        Function *getMax()* returns max value of channel *ch*.
        
        Args:
            ch (int): channel number (default: 1)
            
            verbose (bool): prints max value if set (default: True)
            
        Returns:
            (float): max of channel *ch* in *V*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe MAXImum')
        maxi = self._visaAsk('MEASUrement:IMMed:VALue?')
        maxi = float(maxi)
        maxiUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' max value: '+str(maxi)+' '+maxiUnit[1:-2])
        return maxi
        
        
    def getMean(self, ch=1, verbose=True):
        """
        Function *getMean()* returns arithmetic mean of channel *ch*.
        
        Args:
            ch (int): channel number(s) (default: 1)
            
            verbose (bool): prints mean value if set (default: True)
            
        Returns:
            (float): arithmetic of channel *ch* in *V*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe MEAN')
        mean = self._visaAsk('MEASUrement:IMMed:VALue?')
        mean = float(mean)
        meanUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' arithmetic mean: '+str(mean)+' '+meanUnit[1:-2])
        return mean
        
        
    def getMedian(self, ch=1, strt=1, end=2500, verbose=True):
        """
        Function *getMedian()* returns median value of *ch*.
        
        Args:
            ch (int): channel number(s) (default: 1)
            
            verbose (bool): prints median value if set (default: True)
            
        Returns:
            (float): median of channel *ch* in *V*
        
        """
        self._chkOsciAquiParams(ch, strt, end)
        self._setParam(ch, strt, end)
        x,y=self._getData(strt,end)
        median = np.median(y)
        self._visaWrite("DATa:SOUrce CH"+np.str(ch)) # set last successful channel as target
        medianUnit = self._visaAsk("WFMPre:YUNit?")[1:2]     # units that the y axis are in
        if verbose: print('TekTDS2000: Channel '+str(ch)+' median: '+str(median)+' '+medianUnit)
        return median
        
        
    def getCRms(self, ch=1, verbose=True):
        """
        Function *getCRms()* the true Root Mean Square voltage of the first 
        complete cycle in the waveform of channel *ch*.
        
        Args:
            ch (int): channel number (default: 1)
            
            verbose (bool): prints cyclic root-mean-sqare (RMS) value if set (default: True)
            
        Returns:
            (float): cyclic root-mean-sqare (RMS) of *ch* in *V*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe CRMs')
        rms = self._visaAsk('MEASUrement:IMMed:VALue?')
        rms = float(rms)
        rmsUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' cyclic root-mean-sqare (CRMS): '+str(rms)+' '+rmsUnit[1:-2])
        return rms
                
        
    def getUpp(self, ch=1, verbose=True):
        """
        Function *getUpp()* returns the absolute difference between the 
        maximum and minimum amplitude (Upp) of *ch*.
        
        Args:
            ch (int): channel number(s) (default: 1)
            
            verbose (bool): prints Upp value if set (default: True)
            
        Returns:
            (float): Upp of channel *ch* in *V*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe PK2pk')
        pkpk = self._visaAsk('MEASUrement:IMMed:VALue?')
        pkpk = float(pkpk)
        pkpkUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' U Pk-Pk: '+str(pkpk)+' '+pkpkUnit[1:-2])
        return pkpk
        
        
    def getPeriod(self, ch=1, verbose=True):
        """
        Function *getPeriod()* returns the duration, in seconds, of the first
        complete cycle in the waveform. of channel *ch*.
        
        Args:
            ch (int): channel number (default: 1)
            
            verbose (bool): prints period value if set (default: True)
            
        Returns:
            (float): period of *ch* in *s*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe PERIod')
        period = self._visaAsk('MEASUrement:IMMed:VALue?')
        period = float(period)
        periodUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' period: '+str(period)+' '+periodUnit[1:-2])
        return period
        
        
    def getFreq(self, ch=1, verbose=True):
        """
        Function *getFreq()* returns frequency of channel *ch*.
        
        Args:
            ch (int): channel number (default: 1)
            
            verbose (bool): prints frequency value if set (default: True)
            
        Returns:
            (float): frequency of *ch* in *Hz*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe FREQuency')
        freq = self._visaAsk('MEASUrement:IMMed:VALue?')
        freq = float(freq)
        freqUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' frequency: '+str(freq)+' '+freqUnit[1:-2])
        return freq
        
        
    def getRiseTime(self, ch=1, verbose=True):
        """
        Function *getRiseTime()* returns the rise time between 10% and 90% of 
        the first rising edge of the waveform of channel *ch*. Rising edge 
        must be displayed to measure. The oscilloscope automatically calculates 
        the 10% and 90% measurement points. 
        
        Args:
            ch (int): channel number (default: 1)
            
            verbose (bool): prints rise time value if set (default: True)
            
        Returns:
            (float): rise time of *ch* in *s*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe RISe')
        riseTime = self._visaAsk('MEASUrement:IMMed:VALue?')
        riseTime = float(riseTime)
        riseTimeUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' rise time: '+str(riseTime)+' '+riseTimeUnit[1:-2])
        return riseTime
        
        
    def getFallTime(self, ch=1, verbose=True):
        """
        Function *getFallTime()* returns the fall time between 90% and 10% of 
        the first falling edge of the waveform of channel *ch*. Falling edge 
        must be displayed to measure. The oscilloscope automatically 
        calculates the 10% and 90% measurement points. 
        
        Args:
            ch (int): channel number (default: 1)
            
            verbose (bool): prints fall time value if set (default: True)
            
        Returns:
            (float): fall time of *ch* in *s*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe FALL')
        fallTime = self._visaAsk('MEASUrement:IMMed:VALue?')
        fallTime = float(fallTime)
        fallTimeUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' rise time: '+str(fallTime)+' '+fallTimeUnit[1:-2])
        return fallTime
        
        
    def getPWidth(self, ch=1, verbose=True):
        """
        Function *getFallTime()* returns the positive pulse width between 
        the first rising edge and the next falling edge at the waveform 50% 
        level of channel *ch*. Rising and falling edges must be displayed to 
        measure. The oscilloscope automatically calculates the 50% measurement 
        point.
        
        Args:
            ch (int): channel number (default: 1)
            
            verbose (bool): prints positive pulse width value if set (default: True)
            
        Returns:
            (float): positive pulse width of *ch* in *s*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe PWIdth')
        pwidth = self._visaAsk('MEASUrement:IMMed:VALue?')
        pwidth = float(pwidth)
        pwidthUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' rise time: '+str(pwidth)+' '+pwidthUnit[1:-2])
        return pwidth
        
        
    def getNWidth(self, ch=1, verbose=True):
        """
        Function *getFallTime()* returns the negative pulse width between the 
        first falling edge and the next rising edge at the waveform 50% level 
        of channel *ch*. Falling and rising edges must be displayed to measure. 
        The oscilloscope automatically calculates the 50% measurement point.
        
        Args:
            ch (int): channel number (default: 1)
            
            verbose (bool): prints negative pulse width value if set (default: True)
            
        Returns:
            (float): negative pulse width of *ch* in *s*
        
        """
        self._chkOsciChParam(ch)
        self._visaWrite('MEASUrement:IMMed:SOUrce CH'+str(ch))
        self._visaWrite('MEASUrement:IMMed:TYPe NWIdth')
        nwidth = self._visaAsk('MEASUrement:IMMed:VALue?')
        nwidth = float(nwidth)
        nwidthUnit = self._visaAsk('MEASUrement:IMMed:UNIts?')
        if verbose: print('TekTDS2000: Channel '+str(ch)+' rise time: '+str(nwidth)+' '+nwidthUnit[1:-2])
        return nwidth
        
        
    def getRecordLength(self, verbose=True):
        """
        Function *getRecordLength()* returns waveform record length as number
        of sampling points.
        
        Args:
            verbose (bool): prints record length if set (default: True)
            
        Returns:
            (float): record length 
        
        """
        recLen = self._visaAsk('HORizontal:RECOrdlength?')
        recLen = int(recLen)
        if verbose: print('TekTDS2000: Record length: '+str(recLen))
        return recLen
        
        
    def getSamplingInterval(self, verbose=True):
        """
        Function *getSamplingInterval()* returns sampling interval.
        
        Args:
            verbose (bool): prints sampling interval if set (default: True)
            
        Returns:
            (float): sampling interval 
        
        """
        sampInt = self._visaAsk('WFMPre:XINcr?')
        sampIntUnit = self._visaAsk('WFMPre:XUNit?')[1:-2]
        sampInt = float(sampInt)
        if verbose: print('TekTDS2000: Sampling interval: '+str(sampInt)+' '+sampIntUnit)
        return sampInt
        
        
    def plot(self, ch=[1,2], strt=1, end=2500, filename='', figsize=(800, 600), dpi=75):
        """
        Function *plot()* plots current oscilloscope channels *ch*.
        
        Args:
            ch (int, list): channel number(s) (default: [1,2])
            
            strt (int): start sample (default: 1)
            
            end (int): end sample (default: 2500)
            
            filename (String): string of filename with file extension (e.g. png) (default: '' - no picture save)
            
            figsize (tuple of int): width, height in pixels (default: figsize=(800, 600))
            
            dpi (int): resolution of the figure (default: 75)
            
        Returns:
            none
        
        """
        if type(ch) is type(1):
            ch=[ch]
        self._chkPlotParams(filename, figsize, dpi)
        lstCh = sys.maxsize
        fig,ax = plt.subplots(figsize=(figsize[0]/dpi, figsize[1]/dpi), dpi=dpi)
        x = [0]
        y = [0]
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0)) # scientific notation (*10^x) for x axis
        for i in range(len(ch)):
            self._chkOsciAquiParams(ch[i], strt, end)
            self._setParam(ch[i], strt, end)
            x,y=self._getData(strt,end)
            if (x[0]==None) and (y[0]==None):
                print("TekTDS2000: WARNING! Channel "+str(ch[i])+" is not active!")
                continue
            lstCh = ch[i]
            ax.plot(x,y, label='Channel '+str(ch[i]))
        if lstCh == sys.maxsize:
            print("TekTDS2000: WARNING! No channel available!")
            plt.close(fig)
            return
        ax.legend()
        ax.grid()
        self._visaWrite("DATa:SOUrce CH"+np.str(lstCh)) # set last successful channel as target
        Xunit = self._visaAsk("WFMPre:XUNit?")[1:2]     # units that the x axis are in
        Yunit = self._visaAsk("WFMPre:YUNit?")[1:2]     # units that the y axis are in
        ax.autoscale(enable=True, axis='x', tight=True)
        ax.set_xlabel('Time ['+Xunit+']')
        ax.set_ylabel('Amplitude ['+Yunit+']')
        if filename != '':
            plt.savefig(filename, dpi=dpi)
        return 


    def plotFft(self, ch=1, fftType=FftType.SINGLE_SIDED, filename='', figsize=(800, 600), dpi=75):
        """
        Function *plot()* plots current oscilloscope channels *ch*.
        
        Args:
            ch (int, list): channel number(s) (default: [1,2])
            
            fftType (FftType): fftType as Enum FftType (SINGLE_SIDED, BOTH_SIDED, BW_200MHZ, BW_20MHZ) (default: FftType.SINGLE_SIDED)
            
            filename (String): string of filename with file extension (e.g. png) (default: '' - no picture save)
            
            figsize (tuple of int): width, height in pixels (default: figsize=(800, 600))
            
            dpi (int): resolution of the figure (default: 75)
            
        Returns:
            none
        
        """
        # parameter asserions
        self._chkOsciChParam(ch)
        self._chkPlotParams(filename, figsize, dpi)
        assert type(fftType) == type(FftType.SINGLE_SIDED), "TekTDS2000: fftType parameter is not of type Enum FftType: %r" % type(fftType)
        
        # figure setup
        fig,ax = plt.subplots(figsize=(figsize[0]/dpi, figsize[1]/dpi), dpi=dpi)
        ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0)) # scientific notation (*10^x) for x axis

        # sample data acquisition        
        self._setParam(ch, 1, 2500)
        x,y=self._getData(1,2500)
        if (x[0]==None) and (y[0]==None):
            print("TekTDS2000: WARNING! Channel "+str(ch)+" is not active!")
            plt.close(fig)
            return
        
        dt = self.getSamplingInterval(False)
        fftLen = len(y)
        spec = np.fft.fft(y)/fftLen
        
        # x values in Hz
        f=np.zeros(fftLen)
        for i in range(0, len(spec)):
            f[i]=i/(fftLen*dt)
        
        # fft type setup
        endIdx = 0
        fftTitle = ''
        if fftType == FftType.SINGLE_SIDED:
            endIdx = np.ceil(fftLen/2)
            fftTitle = 'Single-Sided '
        elif fftType == FftType.BOTH_SIDED:
            endIdx = fftLen
            fftTitle = 'Both-Sided '
        elif fftType == FftType.BW_200MHZ:
            endIdx = np.ceil(200000000*fftLen*dt)
            if endIdx > fftLen:
                print("TekTDS2000: WARNING! Bandwidth is out of rage! Sampling rate is "+str(1/dt)+'. Setting fft plot y axis to both sided!')
                endIdx = fftLen
                fftTitle = 'Both-Sided '
            else:
                fftTitle = 'Bandwidth 200MHz '
        elif fftType == FftType.BW_20MHZ:
            endIdx = np.ceil(20000000*fftLen*dt)
            if endIdx > fftLen:
                print("TekTDS2000: WARNING! Bandwidth is out of rage! Sampling rate is "+str(1/dt)+'. Setting fft plot y axis to both sided!')
                endIdx = fftLen
                fftTitle = 'Both-Sided '
            else:
                fftTitle = 'Bandwidth 20MHz '
        else:
            return
        
        # plot fft
        ax.grid()
        ax.plot(f[0:endIdx],np.abs(spec)[0:endIdx])
        ax.autoscale(enable=True, axis='x', tight=True) 
        ax.set_title(fftTitle+'Amplitude Spectrum $f_s$ = {:.0f}'.format(np.round(1/dt)))
        ax.set_xlabel('Frequency [$Hz$]')
        ax.set_ylabel('$|Y(f)|$')
        
        if filename != '':
            plt.savefig(filename, dpi=dpi)
        return 
        
        
    def saveCsv(self, filename='', ch=[1,2], strt=1, end=2500, delimiter=','):
        """
        Function *saveCsv()* saves channels *ch*. First column contains time 
        values followed by channel data. 
        
        Args:
            filename (String): string of filename with file extension 
            
            ch (int, list): channel number(s) (default: [1,2])
            
            strt (int): start sample (default: 1)
            
            end (int): end sample (default: 2500)
            
            delimiter (String): string of delimiter characters
            
        Returns:
            none
        
        """
        if type(ch) is type(1):
            ch=[ch]
        assert type(filename) is type(''), "TekTDS2000: filename string is not an string: %r" % filename
        assert filename is not '', "TekTDS2000: Wrong filename string: %r" % filename
        assert type(delimiter) is type(''), "TekTDS2000: delimiter string is not an string: %r" % delimiter
        
        lstCh = sys.maxsize
        data = []
        times = []
        x = [0]
        y = [0]

        for i in range(len(ch)):
            self._chkOsciAquiParams(ch[i], strt, end)
            self._setParam(ch[i], strt, end)
            x,y=self._getData(strt,end)
            if (x[0]==None) and (y[0]==None):
                print("TekTDS2000: WARNING! Channel "+str(ch[i])+" is not active!")
                continue
            times = x
            lstCh = ch[i]
            data.append(y)
        if lstCh == sys.maxsize:
            print("TekTDS2000: WARNING! No channel available!")
            return
        data.insert(0, times)
        with open(filename, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter,
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerows(np.asarray(data).T)
        return