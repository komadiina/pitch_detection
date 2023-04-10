import struct
import wave
import numpy as np


def get_samples(path: str):
    wf = wave.Wave_read(path)
    return wf.readframes(wf.getnframes())


def save_copy(waveform: wave.Wave_read, path: str):
    wf_copy = wave.Wave_write(path)
    wf_copy.setnchannels(waveform.getnchannels())
    wf_copy.setsampwidth(waveform.getsampwidth())
    wf_copy.setframerate(waveform.getframerate())

    wf_samples = waveform.readframes(waveform.getnframes())
    wf_copy.writeframes(wf_samples)

    wf_copy.close()


def to_nparray(waveform: wave.Wave_read):
    nchannels = waveform.getnchannels()
    sampwidth = waveform.getsampwidth()
    nframes = waveform.getnframes()
    samprate = waveform.getframerate()
    bit = nframes // samprate

    samples = waveform.readframes(nframes)
    arr = np.zeros((nframes, nchannels))

    for i in range(nframes):
        for j in range(nchannels):
            byte_start = (i * nchannels + j) * sampwidth
            byte_end = byte_start + sampwidth
            byte_chunk = samples[byte_start:byte_end]

            # (TODO): assume 32-bit, 2.0 ** 32 = 32768.0
            sample_value = struct.unpack('<h', byte_chunk)[0] / 32768.0
            arr[i, j] = sample_value

    return arr
