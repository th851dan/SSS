import redlab as rl
import numpy as np
import time
import matplotlib.pyplot as pl

x = np.linspace(0,2 * np.pi,30, endpoint=False)
print(np.sin(x))
while(1):
    for i in x:
        rl.cbVOut(0,0,101,np.sin(i)+2)
        #time.sleep(0.01)

#v4 = np.genfromtxt("v4_Messwert.csv",delimiter=",",skip_header=17)
#x = v4[1000:2250,3:4]
#y = v4[1000:2250,4:5]
#pl.figure(figsize=(11,6))
#pl.xlabel('Zeit in s')
#pl.ylabel('Spannung in V')
#pl.plot(x,y)
#pl.grid()
#pl.savefig('v4neu.png')
#pl.show()


#np.save('5500Hz', a)
#pl.plot(a)
print("Samplerate: " + str(rl.cbInScanRate(0,0,0,8000)))
a = rl.cbVInScan(0,0,0,1000,8000,1)
np.save('5500Hz', a)

index = [10,2000,2750,4000,5500,6000,8000]


for i in index:
    v5 = np.load(str(i)+'Hz.npy')
    pl.plot(v5)
    pl.savefig(str(i) + '.png')
    pl.show()
    
#for i in index:
#    v4 = np.genfromtxt(str(i) + "Os.csv",delimiter=",",skip_header=17)
#    pl.plot(v4)
#    pl.show()
#x = v4[250:2250,3:4]