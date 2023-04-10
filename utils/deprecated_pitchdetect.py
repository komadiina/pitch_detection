import reader as reader
from scipy.fft import fft, fftfreq, fftshift
import matplotlib.pyplot as plt
import numpy as np

wf = reader.wave.Wave_read('data/sample.wav')
properties = wf.getparams()

samples = reader.to_nparray(wf)
samples /= np.max(np.abs(samples))

wf.close()

mono = samples.astype(float)

# If stereo, combine into mono
if len(mono.shape) >= 2:
    if mono.shape[1] == 2:
        for i in range(mono.shape[0]):
            mono[i, 0] += mono[i, 1]
        mono /= np.max(np.abs(mono))

mono = np.resize(mono, (mono.shape[0]))

# https://scistatcalc.blogspot.com/2013/12/fft-calculator.html
# np.savetxt("out/samples.txt", mono)
# np.savetxt("out/zeros.txt", np.zeros((mono.shape[0])))

# Number of samples
N = int(samples.shape[0])

# Sampling frequency
fs = properties.framerate

# Time vector
t = np.arange(0, 1, 1/fs)

window = np.hamming(N)
xw = mono * window

S = fft(mono)
X = fftfreq(N, d=1/fs)

plt.plot(X, np.abs(S))
plt.show()
