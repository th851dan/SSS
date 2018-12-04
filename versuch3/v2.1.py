import numpy as np
import matplotlib.pyplot as plt

def verschieb(hz):
    per = (1/hz)/zeitUnit
    print(per)
    print(per*zeitUnit)

    ind1 = np.argmax(data1)
    ind2 = np.argmax(data2)
    n = int(ind2 / per)
    ind2 = ind2 - n * per

    print(ind1)
    print(ind2)
    verschiebung = (ind2-ind1)*zeitUnit
    print('Verschiebung: ' + str(verschiebung) + 's')
    return(verschiebung)

amp = np.zeros(17)
phase = np.zeros(17)
index = [100,200]
c = 0
for i in index:
    data = np.genfromtxt(str(i) + "Hz.csv", delimiter=",")
    data1 = data[:,1]
    data2 = data[:,2]
    dataz = data[:,0]
    zeitUnit = dataz[1]-dataz[0]
    phase[c] = round(verschieb(i),10)
    amp[c] = np.max(data2)
    c = c + 1
    
