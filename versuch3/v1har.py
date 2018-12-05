#from TekTDS2000 import *
import numpy as np
import matplotlib.pyplot as plt
#scope = TekTDS2000()

#scope.saveCsv(ﬁlename='harleybentonrichtig.csv')
data = np.genfromtxt("harleybentonrichtig.csv", delimiter=",")
datas = data[:,1]
dataz = data[:,0]

ind = np.argmax(datas)
print(ind)
ind2 = np.argmax(datas[ind + 1:]) + ind + 1
print(ind2)
periode = dataz[ind2]-dataz[ind]
print("grper", periode)
gfre = 1/periode
print("grfre", gfre)

sigdauer = 0.005 #5ms
ablen = len(data) #Signallänge
abin = sigdauer / ablen #abtastinterval
abfr = 1 / abin #abtastfrequenz
print("Signaldauer: ", sigdauer)
print("Abtastfrequenz: ", abfr)
print("Signallänge: ", ablen)
print("Abtastintervall: ", abin)


Y = abs(np.fft.fft(datas)) # fft computing and normalization
schw = np.argmax(Y)
Y = Y[range(1250)]
plt.xlabel('Frequenz($Hertz$)')
plt.ylabel('Amplitude($Unit$)')
x = np.linspace(0,abfr/2,1250,endpoint = True)
plt.plot(x,abs(Y))
plt.savefig("Spektrum.png")
plt.show()

plt.xlabel('Zeit($s$)')
plt.ylabel('Amplitude($Unit$)')
plt.plot(dataz,datas)
#plt.savefig('messwerteharmonika.png')

#schw = np.argmax(Y)
print('Grundfrequenz: ', schw/(ablen * abin))
print('Amplitude: ', np.max(Y))



