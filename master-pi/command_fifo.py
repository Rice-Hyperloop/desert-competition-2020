import os
import time
import json

class CommandFIFOReader:
    buffer_size = 128
    buffer = b''

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        if not os.path.exists(self.path):
            os.mkfifo(self.path)

        self.fd = os.open(self.path, os.O_RDONLY | os.O_NONBLOCK)
    
        # clear buffer of existing commands
        while os.read(self.fd, self.buffer_size) != b'':
            pass

        return self

    def get_commands(self):
        while True:
            data = os.read(self.fd, self.buffer_size)

            if data == b'':
                break

            self.buffer += data

        index = self.buffer.rfind(b'\n')

        if index < 0:
            return []

        complete_lines = self.buffer[:index].decode('utf8').split('\n')
        self.buffer = self.buffer[index+1:]
        return [json.loads(line) for line in complete_lines]
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.close(self.fd)

class CommandFIFOWriter:
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        if not os.path.exists(self.path):
            os.mkfifo(self.path)

        self.fd = os.open(self.path, os.O_WRONLY)
        return self

    # write command to FIFO (in string form, not JSON)
    def write_command(self, command_string):
        os.write(self.fd, (command_string + '\n').encode('utf8'))

    def __exit__(self, exc_type, exc_value, exc_traceback):
        os.close(self.fd)

