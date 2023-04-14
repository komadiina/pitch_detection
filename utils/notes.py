import numpy as np

# constant root
root = np.power(2.0, (1.0 / 12.0))

notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
num_notes = len(notes)


def calc_freq(idx, tuning) -> float: return ((root ** idx) * tuning)


def frequencies(tuning: int = 440, octaves: int = 8) -> dict:
    if tuning not in range(432, 447):
        raise ValueError(
            f'Expected default tuning range for A4 [432-446], received {tuning}'
        )
    elif octaves <= 0:
        raise ValueError(
            f'Expected a positive integer for octaves, received {octaves}'
        )

    tuning_idx = 4 * num_notes + 9  # A4 index

    # note-number: frequency
    ftable = {}

    # Calculate lower notes
    for i in range(octaves):
        for j in range(num_notes):
            ftable[f'{notes[j]}{i}'] = np.round(calc_freq(
                i * num_notes + j - tuning_idx, tuning), 2)

    return ftable
