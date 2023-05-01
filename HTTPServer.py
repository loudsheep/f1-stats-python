import http.server
import json
import urllib.parse
from SessionDataDownloader import *


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if parsed_path.path == '/schedule':
            x = get_events_remaining()
            data = {'status': '200', 'data': x}

        elif parsed_path.path == '/':
            if 'param1' in query_params:
                data = {'response': 'This is data for param1.'}
            elif 'param2' in query_params:
                data = {'response': 'This is data for param2.'}
            else:
                data = {'response': 'This is default data.'}
        else:
            self.send_error(404)
            return

        self.send_response(200)

        self.send_header('Content-type', 'application/json')
        self.send_header("Access-Control-Allow-Origin", "*")
        # self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        # self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        # self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        # self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        # self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MyHTTPRequestHandler)
    print('Server is running...')
    httpd.serve_forever()
