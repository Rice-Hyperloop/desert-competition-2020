#!/usr/bin/python3

import serial

# open serial in non-blocking mode
s = serial.Serial('/dev/ttyACM0', 115200)

while True:
    print(s.read_until(b'\xfa'))
