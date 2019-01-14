import redlab as rl
import numpy as np
import time
import matplotlib.pyplot as pl

a = rl.cbVInScan(0,0,0,2000,8000,1)
pl.plot(a)
np.save('8000Hz', a)