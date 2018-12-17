import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def winspek(data):
    st = np.std(data)
    gfen = signal.gaussian(512, std = st * 4)
    g = np.zeros(len(data))
    fft = np.zeros(len(data))
    for i in range(0,len(data),256):
        if (i > len(data) - 512):
            break
        g[i:i+512] = data[i:i+512] * gfen
        fft += abs(np.fft.fft(g))
        a = np.fft.fft(g)
        a = a[range(int(len(a)/2))]
        g = np.zeros(len(data))
    
    fft /= 171 #durch die Anzahl der Windows teilen
    fft = fft[range(int(len(fft)/2))]
    return fft

data = np.load('hoch1abgeschnitten.npy')
mit =  np.zeros(int(len(data)/2))
a = ['hoch', 'tief', 'rechts', 'links']
for j in a:
    for i in range(1,6):
        data = np.load(str(j) + str(i) + 'abgeschnitten.npy')
        mit+=winspek(data)
    mit = mit/5
    plt.figure(figsize=(9,6))
    plt.xlabel('Frequenz($Hertz$)')
    plt.ylabel('Amplitude($Unit$)')
    plt.plot(mit)
    plt.savefig("spektrum_mittel_windows"+str(j)+".png")
    plt.show()
    

