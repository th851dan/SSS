import numpy as np
import matplotlib.pyplot as plt

data = np.load('was_cooles_abgeschnitten.npy')
plt.xlabel('Zeit i  n s')
plt.ylabel('Amplitude')
Zeit = []
for i in range (len(data)):
    Zeit.append(1/len(data) * i)
plt.plot(Zeit,data) 
plt.savefig("v1.png")
plt.show()

#Y = abs(np.fft.fft(data))
#schw = np.argmax(Y)
#Y = Y[range(int(len(Y)/2))]
#abfr = len(Y)
#x = np.linspace(0,22050,22050,endpoint = True)
#plt.xlabel('Frequenz($Hertz$)')
#plt.ylabel('Amplitude($Unit$)')
##x = np.linspace(0,abfr/2,1250,endpoint = True)
#plt.plot(x,abs(Y))
#plt.savefig("Spektrumv1.png")
#plt.show()
st = np.std(data)
from scipy import signal
gfen = signal.gaussian(512, std = st * 4)
g = np.zeros(len(data));
fft = []
for i in range(0,len(data),256):
    if (i > len(data) - 512):
        break
    g[i:i+512] = data[i:i+512] * gfen
    plt.plot(range(len(data)),g)
    g = np.zeros(len(data))
    fft.append(np.fft.fft(g))
plt.show()
print(data(g))
#g = data[0:512]*gfen
#g2 = data[0:512]
#g1 = data[255:767] * gfen
#
#plt.plot(g)
#plt.plot(g2)
#plt.plot(gfen)