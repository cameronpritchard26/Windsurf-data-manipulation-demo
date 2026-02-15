import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class MockHandler(BaseHTTPRequestHandler):
    def _respond(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        body = json.dumps({"message": "implementation pending development"})
        self.wfile.write(body.encode("utf-8"))

    def do_PUT(self):
        content_length = int(self.headers.get("Content-Length", 0))
        self.rfile.read(content_length)
        self._respond()

    def do_GET(self):
        self._respond()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        self.rfile.read(content_length)
        self._respond()

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), MockHandler)
    print("Mock API running on http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
