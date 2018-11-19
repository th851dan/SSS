# -*- coding: utf-8 -*-

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(11,30)
cap.set(10,130)
cap.set(14,0)
cap.set(15,-4)
cap.set(17,4980)

print("framewidth:" + str(cap.get(3)))
print("frameheight:" + str(cap.get(4)))
print("--------------------------------")
print("brightness:" + str(cap.get(10)))
print("contrast:" + str(cap.get(11)))
print("saturation:" + str(cap.get(12)))
print("--------------------------------")
print("gain:" + str(cap.get(14)))
print("exposure:" + str(cap.get(15)))
print("--------------------------------")
print("white_balance:" + str(cap.get(17)))


while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('bildweiss10.png',gray)
        print(np.min(gray),np.max(gray))
        break;
        
cap.release()
cv2.destroyAllWindows()

