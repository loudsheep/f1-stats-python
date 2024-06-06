import random

import requests
import fastf1
from fastf1.plotting import team_color
import os

fastf1.Cache.enable_cache(os.path.join(os.path.dirname(__file__), 'cache'))  # replace with your cache directory


def get_drivers_standings():
    url = "https://ergast.com/api/f1/current/driverStandings.json"
    response = requests.get(url)
    data = response.json()
    drivers_standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']  # noqa: E501
    return drivers_standings


def calculate_max_points_for_remaining_season():
    POINTS_FOR_SPRINT = 8 + 25 + 1  # Winning the sprint, race and fastest lap
    POINTS_FOR_CONVENTIONAL = 25 + 1  # Winning the race and fastest lap

    events = fastf1.events.get_events_remaining()
    # Count how many sprints and conventional races are left
    sprint_events = \
        len(events.loc[events["EventFormat"] == "sprint"]) + len(events.loc[events["EventFormat"] == "sprint_shootout"])
    conventional_events = \
        len(events.loc[events["EventFormat"] == "conventional"])

    # Calculate points for each
    sprint_points = sprint_events * POINTS_FOR_SPRINT
    conventional_points = conventional_events * POINTS_FOR_CONVENTIONAL

    return sprint_points + conventional_points


def calculate_max_championship_position(standings, driver_max_points):
    for _, d in enumerate(standings):
        points = int(d["points"])
        if driver_max_points >= points:
            return int(d["position"])

    return 0


def calculate_who_can_win(driver_standings, max_points):
    LEADER_POINTS = int(driver_standings[0]['points'])

    obj = {}
    for _, driver in enumerate(driver_standings):
        driver_max_points = int(driver["points"]) + max_points
        can_win = 'No' if driver_max_points < LEADER_POINTS else 'Yes'

        max_position = calculate_max_championship_position(driver_standings, driver_max_points)

        obj[driver['Driver']['code']] = {
            "current_points": int(driver['points']),
            "wins": int(driver['wins']),
            "max_points": driver_max_points,
            "can_win": True if can_win == "Yes" else False,
            "max_position": max_position,
            "color": team_color(driver['Constructors'][0]['constructorId'])
        }

    return obj
