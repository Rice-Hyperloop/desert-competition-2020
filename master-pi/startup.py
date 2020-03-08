#!/usr/bin/python3

import json
from random import random
import time
import sys
import os 
from os.path import join, realpath
from arduino import Arduino
from command_fifo import CommandFIFOReader
from state import State

rootpath = realpath(sys.path[0])
data_file_path = join(rootpath, 'dashboard', 'data.json')
tmp_data_file_path = join(rootpath, 'dashboard', 'data.json.tmp')

def write_data(data):
    # write to tmp file and rename to make operation atomic
    with open(tmp_data_file_path, 'w') as tmp_file:
        tmp_file.write(json.dumps(data, default=str))
        tmp_file.write('\n')
        tmp_file.flush()
        os.fsync(tmp_file.fileno())
    os.rename(tmp_data_file_path, data_file_path)
        

command_fifo_path = join(rootpath, 'command_fifo')

with CommandFIFOReader(command_fifo_path) as command_fifo, Arduino('/dev/ttyACM0') as arduino:
    while True:
        for command in command_fifo.get_commands():
            if command['name'] == 'estop':
                # emergency stop
                print('EMERGENCY STOP')
                arduino.set_state(State.FAULT)
            elif command['name'] == 'abort':
                # non-emergency stop
                arduino.set_state(State.SAFE_TO_APPROACH)
            elif command['name'] == 'arm':
                arduino.set_state(State.READY_TO_LAUNCH)
            elif command['name'] == 'launch':
                arduino.set_state(State.LAUNCHING)


        arduino.loop()
        data = arduino.get_data()
        if data:
            write_data(data)
        time.sleep(0.1)
