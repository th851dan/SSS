# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 14:54:14 2018

@author: ds-05
"""

import numpy as np
import cv2

data = cv2.imread('bild1.png')
keil1 = data[24:456,0:100]
cv2.imwrite("keil1.png",keil1)

keil2 = data[24:456,110:235]
cv2.imwrite("keil2.png",keil2)

keil3 = data[24:456,245:375]
cv2.imwrite("keil3.png",keil3)

keil4 = data[24:456,380:505]
cv2.imwrite("keil4.png",keil4)

keil5 = data[24:456,515:640]
cv2.imwrite("keil5.png",keil5)

def MuS(keil, n):
    mittel = np.mean(keil)
    std = np.std(keil)
    print('Mittelwert'+ str(n) +':' + str(mittel))
    print('std'+ str(n) +':' + str(std))
MuS(keil1, 1)
MuS(keil2, 2)
MuS(keil3, 3)
MuS(keil4, 4)
MuS(keil5, 5)
