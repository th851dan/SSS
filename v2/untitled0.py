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
np.abs
mittel1 = np.mean(keil1)
std1 = np.std(keil1)
print('Mittelwert1:' + str(mittel1))
print('std1: ' + str(std1))

mittel2 = np.mean(keil2)
std2 = np.std(keil2)
print('Mittelwert2:' + str(mittel2))
print('std2: ' + str(std2))

mittel3 = np.mean(keil3)
std3 = np.std(keil3)
print('Mittelwert3:' + str(mittel3))
print('std3: ' + str(std3))

mittel4 = np.mean(keil4)
std4 = np.std(keil4)
print('Mittelwert4:' + str(mittel4))
print('std4: ' + str(std4))

mittel5 = np.mean(keil5)
std5 = np.std(keil5)
print('Mittelwert5:' + str(mittel5))
print('std5: ' + str(std5))
print(keil1)