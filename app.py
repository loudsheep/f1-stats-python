import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from SessionDataDownloader import *
from StandingsDownloader import *
from WDC_possible_winners import *
from GeneralStatsDownloader import *

config = {
    "DEBUG": False,
    'JSON_SORT_KEYS': False,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
CORS(app)

HOUR = 60 * 60
DAY = 60 * 60 * 24


@app.route('/')
def index():
    return jsonify({'status': '200', 'data': 'This is default data.'}), 200


@app.route('/schedule')
@cache.cached(timeout=DAY * 3)
def schedule():
    return {'status': '200', 'data': get_events_remaining()}, 200


@app.route('/winners')
@cache.cached(timeout=DAY)
def winners():
    driver_standings = get_drivers_standings()
    points = calculate_max_points_for_remaining_season()
    win = calculate_who_can_win(driver_standings, points)

    return json.dumps({'status': '200', 'data': win}), 200


@app.route('/sessions/<int:year>')
@cache.cached(timeout=DAY * 7)
def sessions(year: int):
    return {'status': '200', 'data': get_past_events(int(year))}, 200


@app.route('/results/<int:year>/<int:event>/<string:session>')
@cache.cached(timeout=DAY)
def results(year: int, event: int, session: str):
    try:
        results = get_session_results(year, event, session)
    except:
        return {'status': '500', 'data': 'Internal server error or no data available'}, 500

    return {'status': '200', 'data': results}, 200


@app.route('/tires/<int:year>/<int:event>/<string:session>')
def tires(year: int, event: int, session: str):
    return jsonify({'status': '200', 'data': get_session_compounds_used(year, event, session)}), 200


@app.route('/laps/<int:year>/<int:event>/<string:session>/<string:driver>')
def laps(year: int, event: int, session: str, driver: str):
    return {'status': '200', 'data': load_chart_data(year, event, session, driver)}, 200


# TODO set year dynamically
@app.route('/lap-leaders')
@cache.cached(timeout=DAY)
def lap_leaders():
    return {'status': '200', 'data': count_laps_finished_as_leader(2023)}, 200


@app.route('/heatmap/<int:year>/<string:category>')
def heatmap(year: int, category: str):
    if category == "points":
        data = get_points_heatmap_data(year)
    elif category == "positions":
        data = get_race_position_heatmap_data(year)
    elif category == "qualifying":
        data = get_qualifying_position_heatmap_data(year)
    else:
        return {'status': '400', 'data': 'Unknown category: ' + category}, 400

    return {'status': '200', 'data': data}, 200


@app.route('/telemetry/<int:year>/<int:event>/<string:session>/<string:driver>/<int:lap>')
def telemetry(year: int, event: int, session: str, driver: str, lap: int):
    return {'status': '200', 'data': load_lap_telemetry(year, event, session, driver, lap)}, 200


if __name__ == '__main__':
    app.run()
