"""
Created on Mon Dec 10 12:47:04 2018

@author: ds-05
"""



import pyaudio
import numpy
import matplotlib.pyplot as plt

FORMAT = pyaudio.paInt16
SAMPLEFREQ = 44100
FRAMESIZE = 1024
NOFFRAMES = 220
p = pyaudio.PyAudio()
print("running")

sekunde = [0]*44100

stream = p.open(format=FORMAT,channels=1,rate=SAMPLEFREQ,
                input=True,frames_per_buffer=FRAMESIZE)
data = stream.read(NOFFRAMES*FRAMESIZE)
decoded = numpy.fromstring(data, "Int16");

i=0
while decoded[i] < 100:
    i = i + 1

for k in range(0,44100):
    sekunde[k] = decoded[i+k]
    

numpy.save("t_tief5",decoded)

stream.stop_stream()
stream.close()
p.terminate()
print("done")
plt.plot(sekunde)
plt.xlabel("Messpunkte")
plt.ylabel("AMP")
plt.show()