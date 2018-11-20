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

def norm(list):
    val = 0
    for i in list:
        val += i*i
    betrag = np.sqrt(val)
    normlist = list / betrag
    return normlist
    
def konmaxb(pixel):
    return ((pixel - np.min(pixel)) / (np.max(pixel) - np.min(pixel))) * 255

def konmax(pixel):
    return (pixel / (np.max(pixel) - np.min(pixel))) * 255

mwb = mw('bildschwarz')
#print(konmax(mwb))
mww = mw('bildweiss')
#print(konmax(mww))

cv2.imwrite("kontrastmaxBlack.png", konmaxb(mwb))
cv2.imwrite("kontrastmaxWhite.png", konmax(mww-mwb))

#normw = norm(konmax(mww-mwb))
#print(normw)
a = np.linalg.norm(mww-mwb)
print(a)

#korB = ((bild1 - konmax(mwb)) / (np.max(bild1) - np.min(bild1))) * 255
#cv2.imwrite("kontrastmaxbild.png", korB)
#resWb = ((mww - mwb) / (np.max(mww) - np.min(mww))) * 255
#cv2.imwrite("kontrastmaxWhite.png", resWb)

korW = (bild1 - mwb) / a
cv2.imwrite("Bild1_korrekt.png", a)
cv2.imwrite("mBlack.png", mwb)



