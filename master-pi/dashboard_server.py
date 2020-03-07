#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from os.path import join, realpath
import sys

root_path = join(realpath(sys.path[0]), 'dashboard')
data_path = join(root_path, 'data.json')
command_path = join(root_path, 'data.json')
index_path = join(root_path, 'index.html')

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.handle_dashboard()
        elif self.path == '/data.json':
            self.handle_data()

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
            with open(
            self.send_response(200)

server_address = ('', 8000)
httpd = HTTPServer(server_address, DashboardHandler)
httpd.serve_forever()
