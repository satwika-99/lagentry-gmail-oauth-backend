import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "HTTP server test working!"}
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "ok"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Not found"}
            self.wfile.write(json.dumps(response).encode())

if __name__ == "__main__":
    print("Starting simple HTTP server...")
    print("Server will be available at: http://127.0.0.1:8009")
    
    with socketserver.TCPServer(('', 8009), SimpleHandler) as httpd:
        print("Serving at port 8009...")
        httpd.serve_forever() 