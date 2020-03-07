#!/usr/bin/python3

import json
from random import random
import time
import sys
import os 
from os.path import join, realpath

data_file_path = join(realpath(sys.path[0]), 'dashboard', 'data.json')

def write_data(a, b, c):
    with open(data_file_path, 'w') as data_file:
        data = {
                'a': a,
                'b': b,
                'c': c
        }
        data_file.write(json.dumps(data))
        data_file.write('\n')

while True:
    write_data(random(), random(), random())
    time.sleep(0.2)
