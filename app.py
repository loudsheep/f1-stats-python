import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from SessionDataDownloader import *
from StandingsDownloader import *
from WDC_possible_winners import *

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)


@app.route('/')
def index():
    return jsonify({'status': '200', 'data': 'This is default data.'}), 200


@app.route('/schedule')
def schedule():
    return {'status': '200', 'data': get_events_remaining()}, 200


@app.route('/winners')
def winners():
    driver_standings = get_drivers_standings()
    points = calculate_max_points_for_remaining_season()
    win = calculate_who_can_win(driver_standings, points)

    return json.dumps({'status': '200', 'data': win}), 200


@app.route('/sessions')
def sessions():
    try:
        year = request.args['year']
    except KeyError:
        return {'status': '400', 'data': 'Missing params'}, 400

    return {'status': '200', 'data': get_past_events(int(year))}, 200


@app.route('/results')
def results():
    try:
        year = request.args['year']
        event = request.args['event']
        session = request.args['session']
    except KeyError:
        return {'status': '400', 'data': 'Missing params'}, 400

    try:
        results = get_session_results(int(year), int(event), session)
    except:
        return {'status': '500', 'data': 'Internal server error or no data available'}, 500

    return {'status': '200', 'data': results}, 200


@app.route('/tires')
def tires():
    try:
        year = request.args['year']
        event = request.args['event']
        session = request.args['session']
    except KeyError:
        return {'status': '400', 'data': 'Missing params'}, 400

    return jsonify({'status': '200', 'data': get_session_compounds_used(int(year), int(event), session)}), 200


@app.route('/laps')
def laps():
    try:
        year = request.args['year']
        event = request.args['event']
        session = request.args['session']
        driver = request.args['driver']
    except KeyError:
        return {'status': '400', 'data': 'Missing params'}, 400

    return {'status': '200', 'data': load_chart_data(int(year), int(event), session, driver)}, 200


@app.route('/heatmap')
def heatmap():
    try:
        year = request.args['year']
        category = request.args['category']
    except KeyError:
        return {'status': '400', 'data': 'Missing params'}, 400

    if category == "points":
        data = get_points_heatmap_data(int(year))
    elif category == "positions":
        data = get_race_position_heatmap_data(int(year))
    elif category == "qualifying":
        data = get_qualifying_position_heatmap_data(int(year))
    else:
        return {'status': '400', 'data': 'Unknown category: ' + category}, 400

    return {'status': '200', 'data': data}, 200


@app.route('/telemetry')
def telemetry():
    try:
        year = request.args['year']
        event = request.args['event']
        session = request.args['session']
        driver = request.args['driver']
        lap = request.args['lap']
    except KeyError:
        return {'status': '400', 'data': 'Missing params'}, 400

    return {'status': '200', 'data': load_lap_telemetry(int(year), int(event), session, driver, int(lap))}, 200


if __name__ == '__main__':
    app.run()
