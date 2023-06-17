import datetime
import fastf1
import json
import pytz
import pycountry
import os

utc = pytz.UTC

fastf1.Cache.enable_cache(os.path.join(os.path.dirname(__file__), 'cache'))


def load_lap_telemetry(year, event, ses, driver, lap_number):
    session = fastf1.get_session(year, event, ses)
    session.load(weather=False, messages=False)

    driver_laps = session.laps.pick_driver(driver)

    telemetry = driver_laps.loc[driver_laps['LapNumber'] == lap_number].get_telemetry().add_distance()

    # telemetry["DRS"].replace(
    #     {0: False, 1: False, 2: False, 3: False, 8: False, 10: True, 12: True,
    #      14: True}, inplace=True)

    track_map = telemetry[['X', 'Y']].to_json(orient="records")
    time = telemetry[['Distance', 'Time']].to_json(orient="records").replace("Distance", "X").replace("Time", "Y")
    throttle = telemetry[['Distance', 'Throttle']].to_json(orient="records").replace("Distance", "X").replace(
        "Throttle", "Y")
    brake = telemetry[['Distance', 'Brake']].to_json(orient="records").replace("Distance", "X").replace("Brake", "Y")
    speed = telemetry[['Distance', 'Speed']].to_json(orient="records").replace("Distance", "X").replace("Speed", "Y")
    rpm = telemetry[['Distance', 'RPM']].to_json(orient="records").replace("Distance", "X").replace("RPM", "Y")
    gear = telemetry[['Distance', 'nGear']].to_json(orient="records").replace("Distance", "X").replace("nGear", "Y")
    drs = telemetry[['Distance', 'DRS']].to_json(orient="records").replace("Distance", "X").replace("DRS", "Y")

    obj = {
        "year": year,
        "event": event,
        "session": ses,
        "driver": driver,
        "lap": lap_number,

        "brake": json.loads(brake),
        "drs": json.loads(drs),
        "gear": json.loads(gear),
        "rpm": json.loads(rpm),
        "speed": json.loads(speed),
        "throttle": json.loads(throttle),
        "time": json.loads(time),
        "track_map": json.loads(track_map)
    }
    return obj


def load_chart_data(year, event, session, driver):
    session = fastf1.get_session(year, event, session)
    session.load(telemetry=False, weather=False, messages=False)

    driver_laps = session.laps.pick_driver(driver)
    driver_laps = driver_laps.drop(driver_laps[driver_laps.IsAccurate == False].index)

    return json.loads(driver_laps[['LapNumber', 'LapTime', 'Compound']].to_json(orient="records"))


def add_country_code(pd_row):
    if pd_row['Country'] == 'UAE' or pd_row['Country'] == 'Abu Dhabi':
        return 'AE'
    elif pd_row['Country'] == 'UK':
        return 'GB'
    else:
        return pycountry.countries.search_fuzzy(pd_row['Country'])[0].alpha_2


def get_events_remaining():
    events = fastf1.get_events_remaining()

    events['CountryCode'] = events.apply(lambda x: add_country_code(x), axis=1)
    events = events[
        ['RoundNumber', 'Country', 'Location', 'OfficialEventName', 'EventDate', 'EventName', 'EventFormat',
         'CountryCode']].to_json(
        orient="records", date_format="iso")

    return json.loads(events)


def get_past_events(year: int):
    events = fastf1.get_event_schedule(year, include_testing=False)
    next_event = fastf1.get_events_remaining().iloc[0]

    events = events.loc[events['Session5Date'] < next_event['Session5Date']]
    events = events[
        ['RoundNumber', 'Country', 'Location', 'OfficialEventName', 'EventDate', 'EventName', 'EventFormat']]
    events = events.to_json(
        orient="records", date_format="iso")

    events = json.loads(events)

    for i in events:
        i['Sessions'] = get_sessions_in_event(year, i['RoundNumber'])

    return events


def get_sessions_in_event(year: int, event: int | str):
    event = fastf1.get_event(year, event)

    sessions = []
    for i in range(1, 6):
        if event["Session" + str(i) + "Date"] is None:
            continue
        if event["Session" + str(i) + "Date"].replace(tzinfo=utc) < datetime.datetime.now().replace(tzinfo=utc):
            sessions.append(event["Session" + str(i)])

    return sessions


def get_session_results(year, event, session):
    if session == "SS":
        session = "SQ"
    elif session == "Sprint Shootout":
        session = "Sprint Qualifying"

    session = fastf1.get_session(year, event, session)
    session.load(telemetry=False, weather=False, messages=False, laps=False)

    results = session.results[
        ['DriverNumber', 'Abbreviation', 'FullName', 'TeamName', 'TeamColor', 'Position', 'Status', 'Points']].to_json(
        orient="records", date_format="iso")

    return json.loads(results)
