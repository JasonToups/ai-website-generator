
import http.server
import socketserver
import os
import sys
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Use current directory since we're running from project directory
        super().__init__(*args, directory='.', **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()
    
    def guess_type(self, path):
        # Handle React/JS files properly
        mimetype, encoding = super().guess_type(path)
        if path.endswith('.js'):
            return 'application/javascript', encoding
        elif path.endswith('.jsx'):
            return 'application/javascript', encoding
        elif path.endswith('.ts'):
            return 'application/typescript', encoding
        elif path.endswith('.tsx'):
            return 'application/typescript', encoding
        elif path.endswith('.css'):
            return 'text/css', encoding
        elif path.endswith('.json'):
            return 'application/json', encoding
        return mimetype, encoding
    
    def do_GET(self):
        # For SPA routing, serve index.html for non-file requests
        if not Path('.' + self.path).exists() and not self.path.startswith('/static'):
            self.path = '/index.html'
        return super().do_GET()

# Start server
PORT = 3002
print(f"Starting server on port {PORT}")
print(f"Serving from: {os.getcwd()}")

try:
    with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Server running on http://localhost:{PORT}")
        httpd.serve_forever()
except Exception as e:
    print(f"Server error: {e}")
    import traceback
    traceback.print_exc()
