#!/usr/bin/python3

from serial import Serial
from state import State
import sys

class Arduino:
    def __init__(self, path):
        self.begin_token = b'\xaf'
        self.end_token = b'\xfa'
        self.line_buffer = b''
        self.current_line = None
        self.line_in_progress = False
        self.path = path

    # __enter__ and __exit__ allow using with statement
    def __enter__(self):
        # open serial in non-blocking mode
        self.serial = Serial(self.path, 115200, timeout=0)
        return self

    # should be called each iteration of control loop
    def loop(self):
        waiting = self.serial.in_waiting
        for i in range(0, waiting):
            byte = self.serial.read()
            if (byte == self.begin_token):
                self.line_buffer = b''
                self.line_in_progress = True
            elif (byte == self.end_token):
                if (self.line_in_progress):
                    self.line_in_progress = False
                    self.current_line = self.line_buffer
            else:
                self.line_buffer += byte

    # get parsed data
    def get_data(self):
        try:
            fields = self.current_line.decode('utf8').split(',')
            name = fields[0]

            if name == 'critical-arduino':
                data = {
                        'name': name,
                        'state': State(int(fields[1])).name,
                        'imu2_accel_x': float(fields[2]),
                        'imu2_accel_y': float(fields[3]),
                        'imu2_accel_z': float(fields[4]),
                        'imu2_gyro_x': float(fields[5]),
                        'imu2_gyro_y': float(fields[6]),
                        'imu2_gyro_z': float(fields[7]),
                        'thrust_valve_opened': bool(int(fields[8])),
                        'levitation_valve_opened': bool(int(fields[9])),
                        'high_speed_solenoid_engaged': bool(int(fields[10])),
                        'low_speed_solenoid_engaged': bool(int(fields[11])),
                        'millis': int(fields[12])
                }
                return data
            else:
                return None
        except:
            print('parse error: ' + str(sys.exc_info()))
            return None

    def set_state(self, state):
        self.serial.write(bytearray([state.value]))

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.serial.close()
