# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:38:39 2018

@author: ds-05
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

decoded = np.load("test.npy")



w, h = 512, 880;
N = 512
signaldauer = 1
x = [0]*N

fft = [[0 for x in range(w)] for y in range(h)] 
frame = [[0 for x in range(w)] for y in range(h)] 
mittel_fft  = [0 for x in range(w)] 
gauß = signal.gaussian(512,std=10)

for i in range(0,880):
    if i == 879:
        for k in range(0,256):
            frame[i][k] = decoded[i*256+k]
    else:
        for k in range(0,512):
            frame[i][k] = decoded[i*256+k]
            fft[i] = np.fft.fft(frame[i]*gauß)
            

for i in range(0,880):
    mittel_fft=fft[i]+mittel_fft

for i in range(0,N):
    x[i] = i/signaldauer
  
#mittel_fft = mittel_fft/880

plt.plot(gauß)
    