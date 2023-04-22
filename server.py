import http.server
import socketserver
import api
import json

PORT = 8080

class MyHandler(http.server.SimpleHTTPRequestHandler):
    pass

class APIHandler(MyHandler):
    get_endpoints = {
        '/get_status': api.get_status
    }

    post_endpoints = {
        '/post_status': api.post_status
    }

    def do_GET(self):
        response = self.get_endpoints.get(self.path, api.get_404)
        response_json = json.dumps(response()).encode()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_json)

    def do_POST(self):
        response = self.post_endpoints.get(self.path, api.post_404)
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        response_json = json.dumps(response(data)).encode()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response_json)

Handler = APIHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()