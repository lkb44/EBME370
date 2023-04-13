import array
import board
import audiobusio
import ulab
from ulab import numpy as np
fft_size = 256

# Add the TileGrid to the Gr
# instantiate board mic
mic = audiobusio.PDMIn(board.GP3, board.GP2,sample_rate=16000, bit_depth=16)

#use some extra sample to account for the mic startup
samples_bit = array.array('H', [0] * (fft_size+3))

# Main Loop
def main():
    max_all = 10

    while True:
        mic.record(samples_bit, len(samples_bit))
        samples = np.array(samples_bit[3:])
        spectrogram1 = ulab.utils.spectrogram(samples)
        # spectrum() is always nonnegative, but add a tiny value
        # to change any zeros to nonzero numbers
        spectrogram1 = np.log(spectrogram1 + 1e-7)
        spectrogram1 = spectrogram1[1:(fft_size//2)-1]
        min_curr = np.min(spectrogram1)
        max_curr = np.max(spectrogram1)

        if max_curr > max_all:
            max_all = max_curr
        else:
            max_curr = max_curr-1

        #print(min_curr, max_all)
        min_curr = max(min_curr, 3)
        # Plot FFT
        data = (spectrogram1 - min_curr)
        # This clamps any negative numbers to zero
        data = data * np.array((data > 0))
        print(max(data))
main()