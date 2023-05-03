import pandas as pd

from fastf1.ergast import Ergast
import fastf1
import json

fastf1.Cache.enable_cache('cache')

def get_season_standings(year: int):
    ergast = Ergast()
    races = ergast.get_race_schedule(year)
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

    return json.loads(results.to_json())
