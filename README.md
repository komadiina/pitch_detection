# PyPitch - a pitch detection tool

--- placeholder ---

### dev-notes:
- NFFT of `8192` gives a ~2Hz margin of error for a 240Hz sine wave, whereas `4096` provides a +-4Hz margin of error.
- Make sure you have all the prerequisites installed (`scipy`, `numpy`, `matplotlib`) --> run `pip install -r requirements.txt`