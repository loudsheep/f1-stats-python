import http.server
import json
import urllib.parse
from SessionDataDownloader import *


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        print(query_params)

        if parsed_path.path == '/schedule':
            data = {'status': '200', 'data': get_events_remaining()}

        elif parsed_path.path == '/telemetry':
            if not "year" in query_params:
                self.send_error(400)
                return
            if not "event" in query_params:
                self.send_error(400)
                return
            if not "session" in query_params:
                self.send_error(400)
                return
            if not "driver" in query_params:
                self.send_error(400)
                return
            if not "lap" in query_params:
                self.send_error(400)
                return

            data = {'status': '200',
                    'data': load_lap_telemetry(int(query_params['year'][0]), int(query_params['event'][0]),
                                               query_params['session'][0], query_params['driver'][0],
                                               int(query_params['lap'][0]))}

        elif parsed_path.path == '/sessions':
            if not "year" in query_params:
                self.send_error(400)
                return

            data = {'status': '200',
                    'data': get_past_events(int(query_params['year'][0]))}

        elif parsed_path.path == '/drivers':
            if not "year" in query_params:
                self.send_error(400)
                return
            if not "event" in query_params:
                self.send_error(400)
                return
            if not "session" in query_params:
                self.send_error(400)
                return

            data = {'status': '200',
                    'data': get_drivers_in_session(int(query_params['year'][0]), int(query_params['event'][0]),
                                                   query_params['session'][0])}

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
        self.end_headers()

        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MyHTTPRequestHandler)
    print('Server is running...')
    httpd.serve_forever()
