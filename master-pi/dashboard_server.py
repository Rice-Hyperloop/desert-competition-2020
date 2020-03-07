#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from os.path import join, realpath
from command_fifo import CommandFIFOWriter
import sys

root_path = realpath(sys.path[0])
data_path = join(root_path, 'dashboard', 'data.json')
index_path = join(root_path, 'dashboard', 'index.html')
command_fifo_path = join(root_path, 'command_fifo')

def write_command(command):
    with CommandFIFOWriter(command_fifo_path) as command_fifo:
        command_fifo.write_command(command)

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.handle_dashboard()
        elif self.path == '/data.json':
            self.handle_data()
        else:
            self.send_response(404)
            self.end_headers()

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
