from TekTDS2000 import *
import numpy as np
import matplotlib.pyplot as plt
#scope = TekTDS2000()

#scope.saveCsv(ﬁlename='harleybentonrichtig.csv')
data = np.genfromtxt("harleybentonrichtig.csv", delimiter=",")
datas = data[:,1]
dataz = data[:,0]

dataz1 = data [1000:1500,0:1]
dataz2 = data [1750:,0:1]

data1 = data [1000:1500,1:2]
data2 = data [1750:,1:2]

#plt.plot(dataz,data1)
#plt.plot(dataz,data1)

#ind = np.argmax(data1)
#ind2 = np.argmax(data2)
#periode = dataz2[ind2]-dataz1[ind]
#gfre = 1/periode

#plt.plot(data)
sigdauer = 0.01 #10ms
ablen = len(data) #Signallänge
abin = sigdauer / ablen #abtastinterval
abfr = 1 / abin #abtastfrequenz


Y = abs(np.fft.fft(datas)) # fft computing and normalization
Y = Y[range(1250)]
plt.xlabel('Frequenz($Hertz$)')
plt.ylabel('Amplitude($Unit$)')
x = np.linspace(0,abfr/2,1250,endpoint = True)

plt.plot(x,abs(Y))
plt.show()
plt.xlabel('Zeit($s$)')
plt.ylabel('Amplitude($Unit$)')
plt.plot(dataz,datas)

schw = np.argmax(Y)
print(np.max(Y))
print(schw/(ablen * abin))



