import redlab as rl
import numpy as np
import time
import matplotlib.pyplot as pl

print("------- einzelne Werte -------------------------")
print("16 Bit Scan: " + str(rl.cbAInScan(0,0,0,13,8000,1)))
print("16 Bit Value: " + str(rl.cbAIn(0,0,1)))
#print("Voltage Value: " + str(rl.cbVIn(0,0,1)))
#print("------- Messreihe -------------------------")
a = rl.cbVInScan(0,0,0,1000,8000,1)
#print("Messreihe: " + str(a))
#pl.plot(a)
#pl.show()
#print("Messreihe: " + str(rl.cbVInScan(0,0,0,300,8000,1) ))
#print("Samplerate: " + str(rl.cbInScanRate(0,0,0,8000)))
#print("------- Ausgabe -------------------------") 
#print("Voltage Value: " + str(rl.cbVOut(0,0,101,2.5)))
x = input("Spannung:")
x = float(x)
rl.cbVOut(0,0,101,x)