def approximate_peaks(peaks, ftable):
    detected_notes = {}

    # Find the closest note to each peak
    for freq in peaks:
        detected: str = min(ftable, key=lambda k: abs(ftable[k]-freq))
        detected_notes[detected[:-1]] = True

    return detected_notes


def save_analytics(peaks, detected_notes):
    with open('out/peaks.txt', 'w') as f:
        f.write("Detected frequency peaks [Hz]:\n")
        for peak in peaks:
            f.write(f'-> \t{peak}\n')

        f.write("\nApproximated notes:\n")
        for note, _ in detected_notes.items():
            f.write(f'-> \t{note}\n')


def save_to_file(data, filename, header: str = ""):
    with open(filename, 'w') as f:
        f.write(header)
        f.write(data)
