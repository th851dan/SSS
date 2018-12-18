import pyaudio 
import numpy as np
import matplotlib.pyplot as plt
FORMAT = pyaudio.paInt16
SAMPLEFREQ = 44100
FRAMESIZE = 1024
NOFFRAMES = 220
INPUT_BLOCK_TIME = 0.05 
INPUT_FRAMES_PER_BLOCK = int(SAMPLEFREQ*INPUT_BLOCK_TIME)
p = pyaudio.PyAudio()
print('running')
stream = p.open(format=FORMAT,channels=1,rate=SAMPLEFREQ, input=True,frames_per_buffer=FRAMESIZE)
data = stream.read(NOFFRAMES*FRAMESIZE) 
decoded = np.fromstring(data, 'Int16');
string = 'hoch4'
np.save(string,decoded)
sec = len(decoded) / SAMPLEFREQ

plt.xlabel('Zeit in s')
plt.ylabel('Amplitude')
Zeit = []
for i in range (len(decoded)):
    Zeit.append(sec/len(decoded) * i)
plt.plot(Zeit,decoded) 
plt.show()

trigger = 0.1 * np.max(decoded)

j = 0

for i in decoded:
    j = j + 1
    if np.abs(i) > trigger:
        decoded = decoded[j:j+SAMPLEFREQ]
        break
np.save(string+'abgeschnitten',decoded)

stream.stop_stream() 
stream.close() 
p.terminate() 
print('done') 
plt.xlabel('Zeit in s')
plt.ylabel('Amplitude')
Zeit = []
for i in range (len(decoded)):
    Zeit.append(1/len(decoded) * i)
plt.plot(Zeit,decoded) 
plt.show()

spek = abs(np.fft.fft(decoded))
plt.plot(spek)
