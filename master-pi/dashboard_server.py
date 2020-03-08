#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from os.path import join, realpath, exists, splitext
from command_fifo import CommandFIFOWriter
from collections import defaultdict
import sys

root_path = realpath(sys.path[0])
data_path = join(root_path, 'dashboard', 'data.json')
index_path = join(root_path, 'dashboard', 'index.html')
command_fifo_path = join(root_path, 'command_fifo')

def write_command(command):
    with CommandFIFOWriter(command_fifo_path) as command_fifo:
        command_fifo.write_command(command)

content_types = defaultdict(lambda: 'text/plain')
content_types['.js'] = 'text/javascript'
content_types['.css'] = 'text/css'
content_types['.html'] = 'text/html'
content_types['.json'] = 'application/json'

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

        file_path = join(root_path, 'dashboard') + self.path
        print('accessing...' + file_path)

        if not exists(file_path):
            self.send_response(404)
            self.end_headers()
            return

        with open(file_path, 'rb') as file:
            self.send_response(200)
            _, ext = splitext(file_path)
            content_type = content_types[ext];
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(file.read())

    def handle_data(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        with open(data_path, 'rb') as data:
            self.wfile.write(data.read())

    def handle_dashboard(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(index_path, 'rb') as index:
            self.wfile.write(index.read())

    def do_POST(self):
        if self.path == '/send_command':
            self.send_response(200)
            body_length = int(self.headers['Content-Length'])
            command = self.rfile.read(body_length).decode('utf8')
            self.end_headers()
            write_command(command)
            self.wfile.write(b'COMMAND RECEIVED')
        else:
            self.send_response(404)
            self.end_headers()

server_address = ('', 8000)
httpd = HTTPServer(server_address, DashboardHandler)
httpd.serve_forever()
