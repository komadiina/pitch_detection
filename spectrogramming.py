import utils.reader as reader
from scipy.fft import fft, fftfreq, fftshift
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

wf = reader.wave.Wave_read('data/sample.wav')
properties = wf.getparams()

samples = reader.to_nparray(wf)
samples /= np.max(np.abs(samples))

wf.close()
mono = samples

# If stereo, combine into mono
if len(mono.shape) >= 2:
    if mono.shape[1] == 2:
        for i in range(mono.shape[0]):
            mono[i, 0] += mono[i, 1]
        mono /= np.max(np.abs(mono))

mono = np.resize(mono, (mono.shape[0]))

fs = properties.framerate
duration = float(properties.nframes / properties.framerate)

t = np.linspace(0.0, duration, int(fs * duration), endpoint=False)
f, t, Sxx = signal.spectrogram(mono, fs, nfft=4096)

plt.pcolormesh(t, f, 10 * np.log10(Sxx),  cmap='viridis')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
