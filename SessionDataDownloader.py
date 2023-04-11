import datetime
import fastf1
import json

fastf1.Cache.enable_cache('cache')


def load_lap_telemetry(year, event, ses, driver, lap_number):
    session = fastf1.get_session(year, event, ses)
    session.load()

    driver_laps = session.laps.pick_driver(driver)

    telemetry = driver_laps.loc[driver_laps['LapNumber'] == lap_number].get_telemetry().add_distance()

    telemetry["DRS"].replace(
        {0: False, 1: False, 2: False, 3: False, 8: False, 10: True, 12: True,
         14: True}, inplace=True)

    track_map = telemetry[['X', 'Y']].to_json(orient="records")
    time = telemetry[['Distance', 'Time']].to_json(orient="records")
    throttle = telemetry[['Distance', 'Throttle']].to_json(orient="records")
    brake = telemetry[['Distance', 'Brake']].to_json(orient="records")
    speed = telemetry[['Distance', 'Speed']].to_json(orient="records")
    rpm = telemetry[['Distance', 'RPM']].to_json(orient="records")
    gear = telemetry[['Distance', 'nGear']].to_json(orient="records")
    drs = telemetry[['Distance', 'DRS']].to_json(orient="records")

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
    session.load()

    driver_laps = session.laps.pick_driver(driver)
    # driver_laps['DriverColor'] = plotting.driver_color(driver)

    return json.loads(driver_laps[['LapNumber', 'LapTime', 'Compound']].to_json(orient="records"))


def get_events_remaining():
    events = fastf1.get_events_remaining()
    events = events[
        ['RoundNumber', 'Country', 'Location', 'OfficialEventName', 'EventDate', 'EventName', 'EventFormat']].to_json(
        orient="records", date_format="iso")

    return json.loads(events)


def get_past_events(year: int):
    events = fastf1.get_event_schedule(year, include_testing=False)
    next_event = fastf1.get_events_remaining().iloc[0]

    events = events.loc[events['Session5Date'] < next_event['Session5Date']]
    events = events[
        ['RoundNumber', 'Country', 'Location', 'OfficialEventName', 'EventDate', 'EventName', 'EventFormat']].to_json(
        orient="records", date_format="iso")

    return json.loads(events)


def get_sessions_in_event(year: int, event: int | str):
    event = fastf1.get_event(year, event)

    sessions = []
    for i in range(1, 6):
        if event["Session" + str(i) + "Date"] < datetime.datetime.now():
            sessions.append(event["Session" + str(i)])

    return json.dumps(sessions)


# print(json.dumps(load_lap_telemetry(2023, 3, 'Qualifying', 'BOT', 11)))
print(json.dumps(load_chart_data(2023, 3, 'Qualifying', 'VER')))
# print(load_events_remaining())
# print(get_sessions_in_event(2023, 3))
