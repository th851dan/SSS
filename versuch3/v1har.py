from TekTDS2000 import *
import numpy as np
import matplotlib.pyplot as plt
scope = TekTDS2000()

#scope.saveCsv(ﬁlename='10kHzk.csv')
data = np.genfromtxt("10kHzk.csv", delimiter=",")
dataz = data [:,0:1] 
data1 = data [:,1:2]
data2 = data [:,2:3]
#plt.plot(dataz,data1)
plt.plot(dataz,data2)

