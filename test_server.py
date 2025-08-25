#!/usr/bin/env python3
"""Simple test server for local development without Docker"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.parse
from pathlib import Path
import os
import sys

class MessengerHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_json({'status': 'ok'})
        elif self.path == '/':
            self.send_file('frontend/index.html', 'text/html')
        elif self.path.startswith('/assets/'):
            # Serve built frontend assets
            file_path = Path('frontend/dist') / self.path[1:]
            if file_path.exists():
                self.send_file(str(file_path))
            else:
                self.send_error(404)
        else:
            self.send_error(404, f"Path not found: {self.path}")
    
    def do_POST(self):
        if self.path == '/auth/register':
            self.send_json({'message': 'Registration endpoint - Docker required for full functionality'})
        else:
            self.send_error(404)
    
    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_file(self, filepath, content_type=None):
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            if content_type:
                self.send_header('Content-type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)

if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    port = 8000
    server = HTTPServer(('127.0.0.1', port), MessengerHandler)
    print(f"Test server running at http://127.0.0.1:{port}")
    print("Note: This is a minimal server. Use Docker for full functionality.")
    server.serve_forever()
