#!/usr/bin/python3

import serial

# open serial in non-blocking mode
s = serial.Serial('/dev/ttyACM0', 9600, timeout=0)

while True:
    print(s.readline())
