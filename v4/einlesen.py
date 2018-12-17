import numpy as np
import matplotlib.pyplot as plt

def fft(data,name):
    plt.figure(figsize=(9,6))
    Y = abs(np.fft.fft(data))
    Y = Y[range(int(len(Y)/2))]
    x = np.linspace(0,22050,22050,endpoint = True)
    plt.xlabel('Frequenz($Hertz$)')
    plt.ylabel('Amplitude($Unit$)')
    plt.plot(x,abs(Y))
    plt.savefig(str(name)+".png")
    plt.show()
    
def winspek(data,name):
    plt.figure(figsize=(9,6))
    plt.xlabel('Frequenz($Hertz$)')
    plt.ylabel('Amplitude($Unit$)')
    st = np.std(data)
    from scipy import signal
    gfen = signal.gaussian(512, std = st * 4)
    g = np.zeros(len(data))
    fft = np.zeros(len(data))
    x = np.linspace(0,22050,22050,endpoint = True)
    for i in range(0,len(data),256):
        if (i > len(data) - 512):
            gfen = signal.gaussian(len(data)-i, std = st * 4)
            g[i:] = data[i:] * gfen
            fft += abs(np.fft.fft(g))
            a = np.fft.fft(g)
            a = a[range(int(len(a)/2))]
            plt.plot(x,abs(a))
            break
        g[i:i+512] = data[i:i+512] * gfen
        fft += abs(np.fft.fft(g))
        a = np.fft.fft(g)
        a = a[range(int(len(a)/2))]
        plt.plot(x,abs(a))
        g = np.zeros(len(data))
    plt.savefig("spektrum_gesamter_windows"+str(name)+".png")
    plt.show()
    fft /= 171 #durch die Anzahl der Windows teilen
    fft = fft[range(int(len(fft)/2))]
    plt.figure(figsize=(9,6))
    plt.xlabel('Frequenz($Hertz$)')
    plt.ylabel('Amplitude($Unit$)')
    plt.plot(x,fft)
    plt.savefig("spektrum_mittel_windows"+str(name)+".png")
    return fft
    
data = np.load('was_cooles_abgeschnitten.npy')
plt.figure(figsize=(9,6))
plt.xlabel('Zeit in s')
plt.ylabel('Amplitude')
Zeit = []
for i in range (len(data)):
    Zeit.append(1/len(data) * i)
plt.plot(Zeit,data)
plt.savefig("v1_abgeschnitten.png")
plt.show()
fft(data,"Amplitudenspektrum")

winspek(data,"v1")
