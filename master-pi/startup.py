#!/usr/bin/python3

import json
from random import random
import time
import sys
import os 
from os.path import join, realpath
from arduino import Arduino

data_file_path = join(realpath(sys.path[0]), 'dashboard', 'data.json')

def write_data(data):
    with open(data_file_path, 'w') as data_file:
        data_file.write(json.dumps(data, default=str))
        data_file.write('\n')

with Arduino('/dev/ttyACM0') as arduino:
    while True:
        arduino.loop()
        data = arduino.get_data()
        write_data(data)
        time.sleep(0.1)
