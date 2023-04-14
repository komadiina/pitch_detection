import utils.reader as reader
import utils.notes as notes
from json import dumps

from scipy.fft import fft, ifft
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


def get_spectrogram(file: str, plot: bool = True):
    wf = reader.wave.Wave_read(file)
    properties = wf.getparams()

    duration = float(properties.nframes / properties.framerate)
    if duration < 0.35:
        wf.close()
        raise ValueError(
            f"Expected a duration of >=350ms, received {duration}s.")

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

    # Sampling rate (default to .wav sampling rate)
    fs = properties.framerate

    duration = float(properties.nframes / properties.framerate)

    # Spectrogram resolution, FFT length (2^n)
    NFFT = 8192

    # Pad the signal with edges to match the FFT length
    if len(mono) < NFFT:
        mono = np.pad(mono, (0, NFFT - len(mono)), 'edge')

    # Apply a window function to the signal
    window = signal.windows.hann(NFFT, sym=False)

    # Time vector
    t = np.linspace(0.0, duration, int(fs * duration), endpoint=False)

    # Sample frequencies, segment times, spectrogram
    f, t, Sxx = signal.spectrogram(mono, fs, window=window, nfft=NFFT)

    if plot == True:
        plt.pcolormesh(t, f, 10 * np.log10(Sxx),  cmap='viridis')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()

    return f, t, Sxx


def analyze_peaks(f, t, spectrogram, plot: bool = True):
    # Calculate the magnitude spectrogram
    spectrum = np.abs(spectrogram)

    # Find the peaks along the frequency axis
    peak_indices, _ = signal.find_peaks(spectrum.max(axis=1), height=0.001)

    db_spectrum = 10 * np.log10(spectrum)

    # Plot the spectrogram and the peaks
    if plot:
        plt.pcolormesh(t, f, db_spectrum, cmap='viridis')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()

    peaks = []
    for i in peak_indices:
        peaks.append(f[i])

    return peaks


if __name__ == '__main__':
    ftable = notes.frequencies()
    print(dumps(ftable, indent=4))

    freqs, time, spectrogram = get_spectrogram(
        'data/sample.wav', plot=False)
    peaks = analyze_peaks(freqs, time, spectrogram, plot=True)

    # Cut off peaks above 7902Hz (B8)
    peaks = [np.round(p, 2) for p in peaks if p <= 7902]
    print(peaks)

    # TODO: Map frequencies to their respective note
    # ...

    with open('peaks.txt', 'w') as f:
        for freq in peaks:
            f.write(f'{freq}\n')
