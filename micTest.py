import array
import audiobusio
import math
import board
import time

# Set up the PDM microphone
mic = audiobusio.PDMIn(board.GP20, board.GP21, sample_rate=16000, bit_depth=16)

samples = array.array('H', [0] * 160)
mic.record(samples, len(samples))

# Define a function to calculate the decibel value
def calculate_db(sample):
    rms = math.sqrt(sum([(sample[i] - 32767) ** 2 for i in range(len(sample))]) / len(sample))
    db = 20 * math.log10(rms / 32767)
    return db

# Define a function to calculate the frequency value
def calculate_freq(sample, sample_rate):
    fft = audiobusio.FFT(sample)
    spectrum = fft.as_magnitude_db()
    peak = 0
    peak_idx = 0
    for i in range(len(spectrum) // 2):
        if spectrum[i] > peak:
            peak = spectrum[i]
            peak_idx = i
    freq = sample_rate * peak_idx / len(spectrum)
    return freq

# Continuously print the decibel and frequency values
while True:
    mic.record(samples, len(samples))
    db = calculate_db(samples)
    freq = calculate_freq(samples, mic.sample_rate)
    print("Decibel value:", db, "Frequency value:", freq)
    time.sleep(0.1)
