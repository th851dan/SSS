import numpy as np
import matplotlib.pyplot as plt

def verschieb(hz):
    per = int((1/hz)/zeitUnit)

    ind1 = np.argmax(data1)
    if (ind1 - per) < 0:
       ind1 = ind1 + per
    ind2 = ind1 - per + np.argmax(data2[ind1-per:ind1])
    
    verschiebung = dataz[ind1] - dataz[ind2]
    plt.plot(dataz[ind1],data1[ind1],"ro")
    plt.plot(dataz[ind2],data2[ind2],"bo")
    print('Verschiebung: ' + str(verschiebung) + 's')
    return(verschiebung)

amp = np.zeros(17)
phase = np.zeros(17)

index = [100,200,300,400,500,700,850,1000,1200,1500,1700,
      2000,3000,4000,5000,6000,10000]
c = 0
for i in index:
    data = np.genfromtxt(str(i) + "Hz.csv", delimiter=",")
    data1 = data[:,1]
    data2 = data[:,2]
    dataz = data[:,0]
    zeitUnit = dataz[1]-dataz[0]
    phase[c] = round(verschieb(i),10)
    amp[c] = np.max(data1)/np.max(data2)

    c = c + 1
    plt.plot(dataz,data1)
    plt.plot(dataz,data2)
    plt.show()
    
print('---------------')   
print(amp)
plt.title('Amptitudengang')
plt.plot(index,amp)
plt.show()
print('---------------')
print(phase)
plt.title('Phasengang')
plt.plot(index,phase)
plt.show()

db = 20*np.log10(amp)
Phasenwinkel = -phase*index*360
print('---------------')
print(db)
print('---------------')
print(Phasenwinkel)
plt.subplot(2,1,1)
plt.title('Bode Diagramm')
plt.semilogx(index,db)
plt.ylabel('Amplitude in dB')
plt.subplot(2,1,2)
plt.semilogx(index,Phasenwinkel)
plt.ylabel('Phase in deg')
plt.xlabel('Frequenz in Hz')

