import utils.notes as notes
from json import dumps
import utils.transforms as transforms
import utils.misc as misc
import utils.reader as reader


if __name__ == '__main__':
    ftable = notes.frequencies(octaves=9, tuning=440)
    misc.save_to_file(dumps(ftable, indent=4),
                      'out/ftable.txt', "A4 = 440Hz\n")
    freqs, time, spectrogram = transforms.get_spectrogram(
        'data/sine.wav', plot=False)
    peaks = transforms.analyze_peaks(freqs, time, spectrogram, plot=False)
    detected_notes = misc.approximate_peaks(peaks, ftable)
    misc.save_analytics(peaks, detected_notes)
