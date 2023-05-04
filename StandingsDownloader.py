import pandas as pd

from fastf1.ergast import Ergast
import fastf1
import json
import os
import datetime

fastf1.Cache.enable_cache('cache')


def get_cached_data_round(year):
    if os.path.exists('./cache/standings/' + str(year) + '.txt'):
        with open('./cache/standings/' + str(year) + '.txt') as f:
            lines = f.readlines()
            round = int(lines[0])
        return round

    return 0


def get_cached_data(year):
    if os.path.exists('./cache/standings/' + str(year) + '.txt'):
        with open('./cache/standings/' + str(year) + '.txt') as f:
            lines = f.readlines()
            data = lines[1]
        return json.loads(data)

    return None


def write_to_cache(year, round, data):
    if not os.path.exists('./cache/standings/'):
        os.makedirs('./cache/standings/')

    with open('./cache/standings/' + str(year) + '.txt', 'w') as f:
        f.writelines([str(round) + '\n', data])


def get_season_standings(year: int):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)

    last_round = 0
    for index, race in races.iterrows():
        if race['raceDate'] < datetime.date.today():
            last_round = race['round']
        else:
            break
        # raceDatetime = datetime.datetime
    cached_data_round = get_cached_data_round(year)

    if cached_data_round >= last_round:
        return get_cached_data(year)

    print("GETTING NEW DATA FOR ROUND " + str(last_round) + " OF " + str(year) + " SEASON")
    results = []

    for rnd, race in races['raceName'].items():
        temp = ergast.get_race_results(season=year, round=rnd + 1)
        if len(temp.content) == 0:
            re = results[-1].copy()
            re['round'] = rnd + 1
            re['race'] = race.removesuffix(' Grand Prix')
            re['points'] = None
            results.append(re)
            continue

        temp = temp.content[0]

        sprint = ergast.get_sprint_results(season=year, round=rnd + 1)
        if sprint.content and sprint.description['round'][0] == rnd + 1:
            temp = pd.merge(temp, sprint.content[0], on='driverCode', how='left')
            temp['points'] = temp['points_x'] + temp['points_y']
            temp.drop(columns=['points_x', 'points_y'], inplace=True)

        temp['round'] = rnd + 1
        temp['race'] = race.removesuffix(' Grand Prix')
        temp = temp[['round', 'race', 'driverCode', 'points']]
        results.append(temp)
    results = pd.concat(results)
    races = results['race'].drop_duplicates()

    results = results.pivot(index='driverCode', columns='round', values='points')

    results['total_points'] = results.sum(axis=1)
    results = results.sort_values(by='total_points', ascending=False)
    results.drop(columns='total_points', inplace=True)

    results.columns = races

    write_to_cache(year, last_round, results.to_json())

    return json.loads(results.to_json())
