# frontend/serve_frontend.py
import http.server
import socketserver
import os

PORT = 8000
WEB_DIR = os.path.dirname(os.path.abspath(__file__)) # Should serve from the 'frontend' directory

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def do_GET(self):
        original_path = self.path
        
        if original_path == '/':
            self.path = '/templates/index.html'
        elif original_path == '/register':
            self.path = '/templates/register.html'
        elif original_path == '/login':
            self.path = '/templates/login.html'
        # For other paths like /static/css/style.css or /static/js/auth.js,
        # SimpleHTTPRequestHandler will serve them directly from the WEB_DIR 
        # (e.g., WEB_DIR/static/css/style.css)
        # So, no specific handling is needed for them here, self.path remains as is.

        # print(f"Serving request: Original='{original_path}', Mapped='{self.path}' relative to '{WEB_DIR}'")
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving frontend at http://localhost:{PORT}")
    print(f"Web directory: {WEB_DIR}")
    httpd.serve_forever()
