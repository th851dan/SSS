# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:20:12 2018

@author: ds-05
"""

import numpy as np
import cv2

bild1 = cv2.imread('bild1.png')

def mw(bild):
    data = []
    datad = []
    for i in range(1,11):
        data.append(cv2.imread(str(bild) + str(i) + '.png'))
    for i in data:
        datad.append(i.astype(float))
    mw = np.zeros(datad[0].shape)
    for i in range(0,480):
        for j in range(0,640):
            for k in range(0,10):
                mw[i,j] += datad[k][i,j]
    for i in range(0,480):
        for j in range(0,640):
            mw[i,j] /= 10
    return mw
mwb = mw('bildschwarz')
mww = mw('bildweiss')

korB = bild1 - mwb
cv2.imwrite("korBv2.png", korB)
resWb = mww - mwb
cv2.imwrite("resWbv3.png", resWb)

#
#for i in range(1,11):
#    white.append(cv2.imread('bildweiss'+str(i)+'.png'))
#wmw = np.zeros(data[0].shape)
#for i in range(0,480):
#    for j in range(0,640):
#        for k in range(0,10):
#            wmw[i,j] += data[k][i,j]
#for i in range(0,480):
#    for j in range(0,640):
#        wmw[i,j] /= 10
# 
#
#val = 0
#for i in a:
#    val += i*i
#print (math.sqrt(val))
#a = (1 + 1j)
#print(np.absolute(a))
