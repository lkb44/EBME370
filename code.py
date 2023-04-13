# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import time
import array
import math
import board
import audiobusio
import digitalio
import rtc
import adafruit_adxl34x
import busio
import ulab as np


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

output_pin = digitalio.DigitalInOut(board.GP8)
output_pin.direction = digitalio.Direction.OUTPUT
LEDB_pin = digitalio.DigitalInOut(board.GP21)
LEDB_pin.direction = digitalio.Direction.OUTPUT
LEDG_pin = digitalio.DigitalInOut(board.GP9)
LEDG_pin.direction = digitalio.Direction.OUTPUT
LEDR_pin = digitalio.DigitalInOut(board.GP28)
LEDR_pin.direction = digitalio.Direction.OUTPUT
i2c = busio.I2C(board.GP7,board.GP6)
r = rtc.RTC()

# Main program
mic = audiobusio.PDMIn(board.GP3, board.GP2, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 256)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
prev_acceleration = accelerometer.acceleration
recording = False  # Flag to indicate whether recording is in progress or not

while True:
    current_acceleration = accelerometer.acceleration
    a = current_acceleration[0] > prev_acceleration[0] + 0.1 and current_acceleration[1] < prev_acceleration[1] - 0.1 and current_acceleration[2] > prev_acceleration[2] + 1
    #print("%f %f %f" % accelerometer.acceleration)
    if a and not recording:
        current_time = r.datetime
        print(accelerometer.acceleration, current_time)
        LEDR_pin.value = True
        time.sleep(0.1)
        LEDR_pin.value = False
        time.sleep(0.1)
        start_time = time.monotonic()
        magnitudes = []
        recording = True  # Set flag to True to start recording
        while time.monotonic() - start_time <= 5:
            mic.record(samples, len(samples))
            magnitude = normalized_rms(samples)
            magnitude = 0.0825*magnitude
            magnitude = 0.9936*math.e(magnitude)
            magnitudes.append(magnitude)
        num_above_threshold = sum([1 for mag in magnitudes if mag > 400])
        print(max(magnitudes))
        if num_above_threshold >= 30:
            LEDG_pin.value = True
            time.sleep(1)
            LEDG_pin.value = False
            time.sleep(0.2)
            output_pin.value = True
            time.sleep(1)
            output_pin.value = False
            time.sleep(0.2)
            output_pin.value = True
            time.sleep(0.2)
            output_pin.value = False
            time.sleep(0.2)
        else:
            LEDB_pin.value = not LEDB_pin.value
        time.sleep(0.2)
        LEDB_pin.value = 0
        time.sleep(1)
        recording = False  # Set flag to False to indicate that recording has ended
            
            
                    
                
            
            
        
        