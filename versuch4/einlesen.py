# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:12:09 2018

@author: ds-05
"""

import numpy as np
import matplotlib.pyplot as plt

decoded = np.load("test.npy")
N = 512
sekunde = [0]*44100
i=0
x = [0]*N

while decoded[i] < 50:
    i = i + 1

for k in range(0,44100):
    sekunde[k] = decoded[i+k]


fft = np.fft.fft(sekunde)
signaldauer = 1

for i in range(0,N):
    x[i] = i/signaldauer
plt.plot(x,np.abs(fft[:N]))
#plt.plot(decoded)