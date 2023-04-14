import board
import busio
import digitalio
import storage
import adafruit_sdcard
import os

# Use an SPI bus on specific pins:
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)

# For breakout boards, you can choose any GPIO pin that's convenient:
cs = digitalio.DigitalInOut(board.GP17)

# Create an SDCard object
sdcard = adafruit_sdcard.SDCard(spi, cs)

# Mount the filesystem
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Change directory to the SD card
os.chdir("/sd")

# Open a file for writing
with open("test.txt", "w") as f:
    # Write some data to the file
    f.write("Hello, World!")

# Check that the file was created
print(os.listdir())