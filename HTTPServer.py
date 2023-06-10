import datetime
import http.server
import json
import urllib.parse
from SessionDataDownloader import *
from StandingsDownloader import *
from WDC_possible_winners import *


def write_error_log(message):
    date = datetime.datetime.now()
    with open('error.log', 'a') as f:
        f.write(str(date) + " " + str(message) + "\n")


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        try:
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

            elif parsed_path.path == '/results':
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
                        'data': get_session_results(int(query_params['year'][0]), int(query_params['event'][0]),
                                                    query_params['session'][0])}

            elif parsed_path.path == '/heatmap':
                if not "year" in query_params:
                    self.send_error(400)
                    return
                if not "category" in query_params:
                    self.send_error(400)
                    return

                if query_params['category'][0] == "points":
                    data = {'status': '200',
                            'data': get_points_heatmap_data(int(query_params['year'][0]))}
                elif query_params['category'][0] == "positions":
                    data = {'status': '200',
                            'data': get_race_position_heatmap_data(int(query_params['year'][0]))}
                elif query_params['category'][0] == "qualifying":
                    data = {'status': '200',
                            'data': get_qualifying_position_heatmap_data(int(query_params['year'][0]))}

                else:
                    self.send_error(400)
                    return

            elif parsed_path.path == '/winners':
                driver_standings = get_drivers_standings()
                points = calculate_max_points_for_remaining_season()
                data = {'status': '200',
                        'data': calculate_who_can_win(driver_standings, points)}

            elif parsed_path.path == '/laps':
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

                data = {'status': '200',
                        'data': load_chart_data(int(query_params['year'][0]), int(query_params['event'][0]),
                                                query_params['session'][0], query_params['driver'][0])}

            elif parsed_path.path == '/':
                data = {'status': '200', 'data': 'This is default data.'}
            else:
                self.send_error(404)
                return

            self.send_response(200)

            self.send_header('Content-type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            write_error_log(e)
            self.send_error(500)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()


if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, MyHTTPRequestHandler)
    print('Server is running...')
    httpd.serve_forever()
