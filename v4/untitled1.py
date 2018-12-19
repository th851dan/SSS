import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def winspek(data,name):
    g = np.zeros(len(data))
    for i in range(0,len(data),256):
        
        if (i > len(data) - 512):
            st = np.std(data[i:])
            gfen = signal.gaussian(len(data)-i, std = st * 4)
            g[i:] = data[i:] * gfen
            plt.plot(Zeit,g)
            break
        st = np.std(data[i:i+512])
        gfen = signal.gaussian(512, std = st * 4)
        g[i:i+512] = data[i:i+512] * gfen
        plt.plot(Zeit,g)
        g = np.zeros(len(data))

    
data = np.load('was_cooles/was_cooles_abgeschnitten.npy')
plt.figure(figsize=(9,6))
plt.xlabel('Zeit in s')
plt.ylabel('Amplitude')
Zeit = []
for i in range (len(data)):
    Zeit.append(1/len(data) * i)
plt.plot(Zeit,data)
plt.show()

plt.figure(figsize=(9,6))
plt.xlabel('Frequenz($Hertz$)')
plt.ylabel('Amplitude($Unit$)') 
winspek(data,"v1")