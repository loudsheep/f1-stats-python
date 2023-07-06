import fastf1
from fastf1.ergast import Ergast
from fastf1.plotting import team_color, driver_color
import pandas as pd
import os
import json

fastf1.Cache.enable_cache(os.path.join(os.path.dirname(__file__), 'cache'))


def get_cached_data_round(year, cache_name):
    file_path = os.path.join(os.path.dirname(__file__), 'cache')
    if os.path.exists(file_path + '/' + cache_name + '/' + str(year) + '.txt'):
        with open(file_path + '/' + cache_name + '/' + str(year) + '.txt') as f:
            lines = f.readlines()
            round = int(lines[0])
        return round

    return 0


def get_cached_data(year, cache_name):
    file_path = os.path.join(os.path.dirname(__file__), 'cache')
    if os.path.exists(file_path + '/' + cache_name + '/' + str(year) + '.txt'):
        with open(file_path + '/' + cache_name + '/' + str(year) + '.txt') as f:
            lines = f.readlines()
            data = lines[1]
        return json.loads(data)

    return None


def write_to_cache(year, cache_name, round, data):
    file_path = os.path.join(os.path.dirname(__file__), 'cache')
    if not os.path.exists(file_path + '/' + cache_name + '/'):
        os.makedirs(file_path + '/' + cache_name + '/')

    with open(file_path + '/' + cache_name + '/' + str(year) + '.txt', 'w') as f:
        f.writelines([str(round) + '\n', data])


def index_of_driver(data, driver):
    for d in range(len(data)):
        if data[d]["driver"] == driver:
            return d
    return -1


def count_laps_finished_as_leader(year):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'race_leader')

    if cached_data_round >= last_round:
        return get_cached_data(year, 'race_leader')

    ######################

    if cached_data_round > 0:
        data = get_cached_data(2023, 'race_leader')
    else:
        data = []

    for round in range(cached_data_round + 1, last_round + 1):
        try:
            session = fastf1.get_session(year, round, 'R')
            session.load(laps=True, telemetry=False, weather=False, messages=False)

            for lap in session.laps.iterrows():
                driver = lap[1]["Driver"]
                team = lap[1]["Team"]
                position = lap[1]["Position"]

                if position == 1:
                    idx = index_of_driver(data, driver)

                    if idx >= 0:
                        data[idx]["laps"] += 1
                    else:
                        data.append({
                            "driver": driver,
                            "laps": 1,
                            "color": driver_color(driver)
                        })
        except:
            write_to_cache(2023, 'race_leader', round - 1, json.dumps(data))

        print("Downloaded data from round:", round)

    write_to_cache(2023, 'race_leader', last_round, json.dumps(data))

    return data


def count_total_wins(year):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'race_wins')

    if cached_data_round >= last_round:
        return get_cached_data(year, 'race_wins')

    ######################

    if cached_data_round > 0:
        data = get_cached_data(2023, 'race_wins')
    else:
        data = []

    for round in range(cached_data_round + 1, last_round + 1):
        try:
            session = fastf1.get_session(year, round, 'R')
            session.load(laps=False, telemetry=False, weather=False, messages=False)

            for lap in session.results.iterrows():
                print(lap)
                driver = lap[1]["Abbreviation"]
                team = lap[1]["TeamName"]
                position = lap[1]["Position"]

                if position == 1:
                    idx = index_of_driver(data, driver)

                    if idx >= 0:
                        data[idx]["wins"] += 1
                    else:
                        data.append({
                            "driver": driver,
                            "wins": 1,
                            "color": driver_color(driver)
                        })
        except:
            write_to_cache(2023, 'race_wins', round - 1, json.dumps(data))

        print("Downloaded data from round:", round)

    write_to_cache(2023, 'race_wins', last_round, json.dumps(data))

    return data


def count_total_podiums(year):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'race_podiums')

    if cached_data_round >= last_round:
        return get_cached_data(year, 'race_podiums')

    ######################

    if cached_data_round > 0:
        data = get_cached_data(2023, 'race_podiums')
    else:
        data = []

    for round in range(cached_data_round + 1, last_round + 1):
        try:
            session = fastf1.get_session(year, round, 'R')
            session.load(laps=False, telemetry=False, weather=False, messages=False)

            for lap in session.results.iterrows():
                # print(lap)
                driver = lap[1]["Abbreviation"]
                team = lap[1]["TeamName"]
                position = int(lap[1]["Position"])

                if position <= 3:
                    idx = index_of_driver(data, driver)

                    if idx >= 0:
                        data[idx]["podiums"] += 1
                    else:
                        data.append({
                            "driver": driver,
                            "podiums": 1,
                            "color": driver_color(driver)
                        })

        except:
            write_to_cache(2023, 'race_podiums', round - 1, json.dumps(data))

        print("Downloaded data from round:", round)

    write_to_cache(2023, 'race_podiums', last_round, json.dumps(data))

    return data


def count_total_pole_positions(year):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'pole_positions')

    if cached_data_round >= last_round:
        return get_cached_data(year, 'pole_positions')

    ######################

    if cached_data_round > 0:
        data = get_cached_data(2023, 'pole_positions')
    else:
        data = []

    for round in range(cached_data_round + 1, last_round + 1):
        try:
            session = fastf1.get_session(year, round, 'Q')
            session.load(laps=False, telemetry=False, weather=False, messages=False)

            for lap in session.results.iterrows():
                # print(lap)
                driver = lap[1]["Abbreviation"]
                team = lap[1]["TeamName"]
                position = int(lap[1]["Position"])

                if position == 1:
                    idx = index_of_driver(data, driver)

                    if idx >= 0:
                        data[idx]["poles"] += 1
                    else:
                        data.append({
                            "driver": driver,
                            "poles": 1,
                            "color": driver_color(driver)
                        })

        except:
            write_to_cache(2023, 'pole_positions', round - 1, json.dumps(data))

        print("Downloaded data from round:", round)

    write_to_cache(2023, 'pole_positions', last_round, json.dumps(data))

    return data