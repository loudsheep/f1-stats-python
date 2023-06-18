import pandas as pd

from fastf1.ergast import Ergast
import fastf1
import json
import os
import pycountry

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


def get_points_heatmap_data(year: int):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'points')

    if cached_data_round >= last_round:
        return get_cached_data(year, 'points')

    rounds = []
    for i in races['round']:
        race = races.loc[i - 1]
        if race['country'] == 'UAE':
            country_code = 'AE'
        elif race['country'] == 'UK':
            country_code = 'GB'
        else:
            country_code = pycountry.countries.search_fuzzy(race['country'])[0].alpha_2

        if race['raceName'][:3] == "Aus":
            race_code = pycountry.countries.search_fuzzy(race['country'])[0].alpha_3
        else:
            race_code = race['raceName'][:3].upper()
        rounds.append({
            'country': race['country'],
            'countryCode': country_code,
            'raceCode': race_code
        })

    standings = ergast.get_driver_standings(year)
    drivers = []
    for i in standings.content[0]['driverCode'].items():
        drivers.append(i[1])

    results = []

    for rnd, race in races['raceName'].items():
        temp = ergast.get_race_results(season=year, round=rnd + 1)
        if len(temp.content) == 0:
            for d in drivers:
                results.append({
                    'driver': d,
                    'race': rounds[rnd]['raceCode'],
                    'value': None
                })
            continue
        temp = temp.content[0]

        sprint = ergast.get_sprint_results(season=year, round=rnd + 1)
        if sprint.content and sprint.description['round'][0] == rnd + 1:
            temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
            temp['points'] = temp['points_x'] + temp['points_y']
            temp.drop(columns=['points_x', 'points_y'], inplace=True)

        temp['race'] = rounds[rnd]['raceCode']
        temp = temp[['race', 'driverCode', 'points']]

        for idx, row in temp.iterrows():
            results.append({
                'driver': row['driverCode'],
                'race': row['race'],
                'value': row['points']
            })

    ret = {
        'races': rounds,
        'drivers': drivers,
        'chartData': results
    }

    write_to_cache(year, 'points', last_round, json.dumps(ret))

    return ret


def get_race_position_heatmap_data(year: int):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'positions')

    if cached_data_round >= last_round:
        return get_cached_data(year, 'positions')

    rounds = []
    for i in races['round']:
        race = races.loc[i - 1]
        if race['country'] == 'UAE':
            country_code = 'AE'
        elif race['country'] == 'UK':
            country_code = 'GB'
        else:
            country_code = pycountry.countries.search_fuzzy(race['country'])[0].alpha_2

        if race['raceName'][:3] == "Aus":
            race_code = pycountry.countries.search_fuzzy(race['country'])[0].alpha_3
        else:
            race_code = race['raceName'][:3].upper()
        rounds.append({
            'country': race['country'],
            'countryCode': country_code,
            'raceCode': race_code
        })

    standings = ergast.get_driver_standings(year)
    drivers = []
    for i in standings.content[0]['driverCode'].items():
        drivers.append(i[1])

    results = []

    for rnd, race in races['raceName'].items():
        temp = ergast.get_race_results(season=year, round=rnd + 1)

        if len(temp.content) == 0:
            for d in drivers:
                results.append({
                    'driver': d,
                    'race': rounds[rnd]['raceCode'],
                    'value': None
                })
            continue

        temp = temp.content[0]
        temp['race'] = rounds[rnd]['raceCode']
        temp = temp[['race', 'driverCode', 'position', 'positionText']]

        for idx, row in temp.iterrows():
            results.append({
                'driver': row['driverCode'],
                'race': row['race'],
                'value': row['position'] if str(row['position']) == row['positionText'] else row['positionText']
            })

    ret = {
        'races': rounds,
        'drivers': drivers,
        'chartData': results
    }

    write_to_cache(year, 'positions', last_round, json.dumps(ret))

    return ret


def get_qualifying_position_heatmap_data(year: int):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'].date() < pd.Timestamp.today().date():
            last_round = race['round']
        else:
            break
    cached_data_round = get_cached_data_round(year, 'quali')

    if cached_data_round >= last_round:
        return get_cached_data(year, 'quali')

    rounds = []
    for i in races['round']:
        race = races.loc[i - 1]
        if race['country'] == 'UAE':
            country_code = 'AE'
        elif race['country'] == 'UK':
            country_code = 'GB'
        else:
            country_code = pycountry.countries.search_fuzzy(race['country'])[0].alpha_2

        if race['raceName'][:3] == "Aus":
            race_code = pycountry.countries.search_fuzzy(race['country'])[0].alpha_3
        else:
            race_code = race['raceName'][:3].upper()
        rounds.append({
            'country': race['country'],
            'countryCode': country_code,
            'raceCode': race_code
        })

    standings = ergast.get_driver_standings(year)
    drivers = []
    for i in standings.content[0]['driverCode'].items():
        drivers.append(i[1])

    results = []

    for rnd, race in races['raceName'].items():
        temp = ergast.get_qualifying_results(season=year, round=rnd + 1)

        if len(temp.content) == 0:
            for d in drivers:
                results.append({
                    'driver': d,
                    'race': rounds[rnd]['raceCode'],
                    'value': None
                })
            continue

        temp = temp.content[0]
        temp['race'] = rounds[rnd]['raceCode']
        temp = temp[['race', 'driverCode', 'position']]

        for idx, row in temp.iterrows():
            results.append({
                'driver': row['driverCode'],
                'race': row['race'],
                'value': row['position']
            })

    ret = {
        'races': rounds,
        'drivers': drivers,
        'chartData': results
    }

    write_to_cache(year, 'quali', last_round, json.dumps(ret))

    return ret

# print(get_race_positions(2022))
# print(get_season_standings(2023))
# print(get_qualifying_position_heatmap_data(2023))