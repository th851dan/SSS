import redlab as rl
import numpy as np
import time
import matplotlib.pyplot as pl
#print("------- einzelne Werte -------------------------")
#print("16 Bit Value: " + str(rl.cbAIn(0,0,1)))
#print("Voltage Value: " + str(rl.cbVIn(0,0,1)))
#print("------- Messreihe -------------------------")
#print("Messreihe: " + str(rl.cbAInScan(0,0,0,300,8000,1) ))
a = rl.cbVInScan(0,0,0,1000,8000,1)
#print("Messreihe: " + str(rl.cbVInScan(0,0,0,300,8000,1) ))
#print("Samplerate: " + str(rl.cbInScanRate(0,0,0,8000)))
#print("------- Ausgabe -------------------------")

#x = np.linspace(0,2 * np.pi,30, endpoint=False)
#print(np.sin(x))
#while(1):
#    for i in x:
#        rl.cbVOut(0,0,101,np.sin(i)+2)
#        time.sleep(0.01)
#np.save('5500Hz', a)
pl.plot(a)
