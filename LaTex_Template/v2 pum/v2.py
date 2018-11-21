# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 16:20:12 2018

@author: ds-05
"""

import numpy as np
import cv2

bild1 = cv2.imread('bild1.png')

def mw(bild): #Bildern einlesen und Mittelwert für jede Pixel bilden
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
    
def konmaxb(pixel):
    return ((pixel - np.min(pixel)) / (np.max(pixel) - np.min(pixel))) * 255

def konmax(pixel):
    return (pixel / (np.max(pixel) - np.min(pixel))) * 255

mwb = mw('bildschwarz') #Mittelwert von Dunkelbildern
cv2.imwrite("mBlack.png", mwb)
cv2.imwrite("kontrastmaxBlack.png", konmaxb(mwb)) #Ausgabe kontrastmaximiertes Dunkelbildes

korBv2 = bild1 - mwb
cv2.imwrite("korrigiertes Bild v2.png", korBv2)

mww = mw('bildweiss') #Mittelwert von Weißbildern
cv2.imwrite("mWhite.png", mww)
cv2.imwrite("kontrastmaxWhite.png", konmax(mww-mwb)) #Ausgabe kontrastmaximiertes Weißbildes
normW = (mww-mwb)/np.mean(mww-mwb) # nomiertes Weißbild
korW = korBv2 / normW
cv2.imwrite("Bild1_korrekt.png", korW)





