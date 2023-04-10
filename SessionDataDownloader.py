import fastf1
import json
import os

fastf1.Cache.enable_cache('cache')  # replace with your cache directory


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


print(load_chart_data(2023, 3, 'Q', 'VER'))
