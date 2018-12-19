import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

    
data = np.load('was_cooles/was_cooles_abgeschnitten.npy')
plt.figure(figsize=(9,6))
plt.xlabel('Zeit in s')
plt.ylabel('Amplitude')
Zeit = []
for i in range (len(data)):
    Zeit.append(1/len(data) * i)
g = []
for i in range(1):
   g[i:i+512] = data[i:i+512] 
   plt.plot(Zeit[:512],g)
   st = np.std(g)
   gfen = signal.gaussian(512, std = 4*st)
   g = g * gfen
   plt.plot(Zeit[:512],g)
   g = np.zeros(len(data))
plt.savefig("window signal.png")
plt.show()
plt.plot(gfen)