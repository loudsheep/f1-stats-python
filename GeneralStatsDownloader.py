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


# ------------ stats ------------ #
def count_laps_finished_as_leader(year):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    # check the cache for saved data
    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'race_leader')

    # if cached data is up-to-date return it
    if cached_data_round >= last_round:
        return get_cached_data(year, 'race_leader')

    ######################

    # else load the cached data and append the latest information to it
    if cached_data_round > 0:
        data = get_cached_data(2023, 'race_leader')
    else:
        data = []

    # for every round in the season
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
                        data[idx]["value"] += 1
                    else:
                        data.append({
                            "driver": driver,
                            "team": team,
                            "value": 1,
                            "color": team_color(team)
                        })
                else:
                    idx = index_of_driver(data, driver)
                    if idx < 0:
                        data.append({
                            "driver": driver,
                            "team": team,
                            "value": 0,
                            "color": team_color(team)
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
                driver = lap[1]["Abbreviation"]
                team = lap[1]["TeamName"]
                position = lap[1]["Position"]

                if position == 1:
                    idx = index_of_driver(data, driver)

                    if idx >= 0:
                        data[idx]["value"] += 1
                    else:
                        data.append({
                            "driver": driver,
                            "team": team,
                            "value": 1,
                            "color": team_color(team)
                        })
                else:
                    idx = index_of_driver(data, driver)
                    if idx < 0:
                        data.append({
                            "driver": driver,
                            "team": team,
                            "value": 0,
                            "color": team_color(team)
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
                        data[idx]["value"] += 1
                    else:
                        data.append({
                            "driver": driver,
                            "team": team,
                            "value": 1,
                            "color": team_color(team)
                        })
                else:
                    idx = index_of_driver(data, driver)
                    if idx < 0:
                        data.append({
                            "driver": driver,
                            "team": team,
                            "value": 0,
                            "color": team_color(team)
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
                        data[idx]["value"] += 1
                    else:
                        data.append({
                            "driver": driver,
                            "team": team,
                            "value": 1,
                            "color": team_color(team)
                        })
                else:
                    idx = index_of_driver(data, driver)
                    if idx < 0:
                        data.append({
                            "driver": driver,
                            "team": team,
                            "value": 0,
                            "color": team_color(team)
                        })

        except:
            write_to_cache(2023, 'pole_positions', round - 1, json.dumps(data))

        print("Downloaded data from round:", round)

    write_to_cache(2023, 'pole_positions', last_round, json.dumps(data))

    return data


def count_top_10_race_finishes(year):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'race_top_10')

    if cached_data_round >= last_round:
        return get_cached_data(year, 'race_top_10')

    ######################

    if cached_data_round > 0:
        data = get_cached_data(2023, 'race_top_10')
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

                if position <= 10:
                    idx = index_of_driver(data, driver)

                    if idx >= 0:
                        data[idx]["value"] += 1
                    else:
                        data.append({
                            "driver": driver,
                            "team": team,
                            "value": 1,
                            "color": team_color(team)
                        })
                else:
                    idx = index_of_driver(data, driver)
                    if idx < 0:
                        data.append({
                            "driver": driver,
                            "team": team,
                            "value": 0,
                            "color": team_color(team)
                        })

        except:
            write_to_cache(2023, 'race_top_10', round - 1, json.dumps(data))

        print("Downloaded data from round:", round)

    write_to_cache(2023, 'race_top_10', last_round, json.dumps(data))

    return data


def best_result(year):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'best_result')

    if cached_data_round >= last_round:
        return get_cached_data(year, 'best_result')

    ######################

    if cached_data_round > 0:
        data = get_cached_data(2023, 'best_result')
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

                idx = index_of_driver(data, driver)

                if idx >= 0:
                    if position < data[idx]["value"]:
                        data[idx]["value"] = position
                else:
                    data.append({
                        "driver": driver,
                        "team": team,
                        "value": position,
                        "color": team_color(team)
                    })

        except:
            write_to_cache(2023, 'best_result', round - 1, json.dumps(data))

        print("Downloaded data from round:", round)

    write_to_cache(2023, 'best_result', last_round, json.dumps(data))

    return data


def worst_result(year):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'worst_result')

    if cached_data_round >= last_round:
        return get_cached_data(year, 'worst_result')

    ######################

    if cached_data_round > 0:
        data = get_cached_data(2023, 'worst_result')
    else:
        data = []

    for round in range(cached_data_round + 1, last_round + 1):
        try:
            session = fastf1.get_session(year, round, 'R')
            session.load(laps=False, telemetry=False, weather=False, messages=False)

            for lap in session.results.iterrows():
                driver = lap[1]["Abbreviation"]
                team = lap[1]["TeamName"]
                position = int(lap[1]["Position"])

                idx = index_of_driver(data, driver)

                if (lap[1]["Status"] != "Finished") and ("Lap" not in lap[1]["Status"]):
                    continue

                if idx >= 0:
                    if position > data[idx]["value"]:
                        data[idx]["value"] = position
                else:
                    data.append({
                        "driver": driver,
                        "team": team,
                        "value": position,
                        "color": team_color(team)
                    })

        except:
            write_to_cache(2023, 'worst_result', round - 1, json.dumps(data))

        print("Downloaded data from round:", round)

    write_to_cache(2023, 'worst_result', last_round, json.dumps(data))

    return data
