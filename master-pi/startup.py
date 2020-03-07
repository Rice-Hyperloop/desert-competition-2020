#!/usr/bin/python3

import json
from random import random
import time
import sys
import os 
from os.path import join, realpath
from arduino import Arduino
from command_fifo import CommandFIFOReader

rootpath = realpath(sys.path[0])
data_file_path = join(rootpath, 'dashboard', 'data.json')

def write_data(data):
    with open(data_file_path, 'w') as data_file:
        data_file.write(json.dumps(data, default=str))
        data_file.write('\n')

def do_command(command):
    if command['name'] == 'estop':
        print('EMERGENCY STOP')

command_fifo_path = join(rootpath, 'command_fifo')

with CommandFIFOReader(command_fifo_path) as command_fifo, Arduino('/dev/ttyACM0') as arduino:
    while True:
        for command in command_fifo.get_commands():
            print('command: ' + str(command))
            do_command(command)

        arduino.loop()
        data = arduino.get_data()
        write_data(data)
        time.sleep(0.1)
