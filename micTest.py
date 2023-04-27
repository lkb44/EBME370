import os
import time
import array
import math
import board
import busio
import storage
import digitalio
import audiobusio
import adafruit_sdcard
import adafruit_datetime as dt

spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs = digitalio.DigitalInOut(board.GP17)

sdcard = adafruit_sdcard.SDCard(spi, cs)

vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Change directory to the SD card
os.chdir("/sd")

# Remove DC bias before computing RMS.
def mean(values):
    return sum(values) / len(values)


def normalized_rms(values):
    minbuf = int(mean(values))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in values
    )

    return math.sqrt(samples_sum / len(values))


# Main program
mic = audiobusio.PDMIn(board.GP20, board.GP21, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 160)

# Open a file for writing
with open("test.csv", "a") as f:
    while True:
        mic.record(samples, len(samples))
        # Get the current date and time
        now = dt.datetime.now()

        # Format the date and time as a string
        timestamp = "{:02}:{:02}:{:02}".format(
            now.hour, now.minute, now.second
        )
        print(timestamp)
        magnitude = normalized_rms(samples)
        print(magnitude)
        os.chdir("/sd")
        # Write some data to the file
        f.write("Decibels: {:.2f}, ".format(magnitude))
        f.write(", ".format(timestamp))
        f.write("\n")
        print(os.listdir())
        time.sleep(1)

