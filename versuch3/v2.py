import numpy as np
import matplotlib.pyplot as plt

def verschieb(hz):
    per = int(round((1/hz)/zeitUnit))
    print(per)
    print(per*zeitUnit)

    ind1 = np.argmax(data1[int(per*0.5):int(per*1.5)])+int(per/2)
    ind2 = np.argmax(data2[int(per*0.5):int(per*1.5)])+int(per/2)

    print((ind1*zeitUnit)+dataz[0])
    print((ind2*zeitUnit)+dataz[0])

    verschiebung = (ind2-ind1)*zeitUnit
    if verschiebung > (per*zeitUnit):
        verschiebung =- (per*zeitUnit)
    if verschiebung < 0:
        verschiebung =+ (per*zeitUnit)
    print('Verschiebung: ' + str(verschiebung) + 's')
    return(verschiebung)

amp = np.zeros(17)
phase = np.zeros(17)
index = [100,200,300,400,500,700,850,1000,1200,1500,1700,
     2000,3000,4000,5000,6000,10000]
c = 0
for i in index:
    data = np.genfromtxt(str(i) + "Hzk.csv", delimiter=",")
    data1 = data[:,1]
    data2 = data[:,2]
    dataz = data[:,0]
    zeitUnit = dataz[1]-dataz[0]
    phase[c] = round(verschieb(i),10)
    amp[c] = np.max(data2)
    c = c + 1
    plt.plot(dataz,data1)
    plt.plot(dataz,data2)
    plt.show()
    
print('---------------')   
print(amp)
plt.subplot(2,1,1)
plt.plot(index,amp)
print('---------------')
print(phase)
plt.subplot(2,1,2)
plt.plot(index,phase)

db = 20*np.log10(amp/np.max(data1))
Phasenwinkel = -phase*index*2*np.pi
print('---------------')
print(db)
print('---------------')
print(Phasenwinkel)

plt.show()
plt.semilogx(amp)
plt.show()
plt.semilogx(phase)
