import reader
from scipy.fft import fft, fftfreq, fftshift
from scipy.signal import blackman
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

wf = reader.wave.Wave_read('untitled.wav')
samples = reader.to_nparray(wf)

# Combine channels into mono (one-dimensional)
mono = np.sum(samples, axis=1).reshape(-1, 1)

# Sample points
N = samples.shape[0]

# Sample spacing, 1:1
T = 1.0 / N

x = np.linspace(0.0, N*T, N, endpoint=False)

yf = fft(mono)
w = blackman(N)
ywf = fft(mono * w)
xf = fftfreq(N, T)[:N]

# Styling
mpl.rcParams['lines.linewidth'] = 1
with plt.style.context('dark_background'): 
    plt.plot(xf[1:N], 2.0/N * np.abs(ywf[1:N]), '-b')
plt.legend(['FFT'])
plt.grid()
plt.show()
