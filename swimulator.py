import json
import requests
from Solvers import ncaaSolver as ns
from Solvers import mcslSolver as ms
import time


def swimulate(team1, team2, gender, age=25, cfg="configs/NCAA.json"):
    # Build a dict of swimmers with their names as keys and a dict of race-time pairs as the value
    # Gender needed for power point calculation
    cfgDict = json.load(open(cfg))
    if cfg=="configs/MCSL.json":
        # Team1 and Team2 for MCSL should just be CSV of team
        team_1_dict = create_mcsl_dict(team1)
        team_2_dict = create_mcsl_dict(team2)
        team_1_lineup, team_2_lineup = calculate_mcsl_lineup(team_1_dict, team_2_dict)

    else:
        team_1_dict = create_ncaa_dict(team1)
        team_2_dict = create_ncaa_dict(team2)
        team_1_lineup, team_2_lineup = calculate_ncaa_lineup(team_1_dict, team_2_dict, gender)

    return lineup_to_string(team_1_lineup, cfgDict) + "\n" + lineup_to_string(team_2_lineup, cfgDict)


# Cols for MCSL: ID, lastName, firstName, age, team, time, sex, distance, event, year, week
# All MCSL race data can be put into a sql database, meaning that to get all the swim dicts we need, we just need a team
# abbreviation and a year. Each swimmer will contain an age
def create_mcsl_dict(team):
    return True


def create_ncaa_dict(team):
    return_dict = {}
    with open(team, 'rb') as f:
        for line in f:
            item = dict(json.loads(line))
            if item["name"] in return_dict.keys():
                return_dict[item['name']][item['event']] = item['time']
            else:
                return_dict[item['name']] = {item['event']: item['time']}
    return return_dict


# To calculate power points, use the highest age in the mcsl age group the swimmer is in
def calculate_mcsl_lineup(team_dict_one, team_dict_two):
    return 1, 2


def calculate_ncaa_lineup(team_dict_one, team_dict_two, gender):

    # First, replace times with power points
    for swimmer in team_dict_one.values():
        for event in swimmer:
            swimmer[event] = calculate_power_points(swimmer[event], event, gender)

    for swimmer in team_dict_two.values():
        for event in swimmer:
            swimmer[event] = calculate_power_points(swimmer[event], event, gender)

    optimized_team_one = ns.ncaa_duel_optimize(team_dict_one, team_dict_two)
    optimized_team_two = ns.ncaa_duel_optimize(team_dict_two, team_dict_one)

    return optimized_team_one, optimized_team_two


def calculate_power_points(time, event_id, gender, age=25):
    url = "https://www.usaswimming.org/api/Times_PowerPointCalculator/CalculatePowerPoints"

    minutes_split = time.split(":")
    if len(minutes_split) == 1:
        minutes = 0
        minutes_split = minutes_split[0]
    else:
        minutes = minutes_split[0]
        minutes_split = minutes_split[1]
    seconds_split = minutes_split.split(".")

    payload = {'DSC[DistanceID]': str(event_id)[1:],
               'DSC[StrokeID]': str(event_id)[0],
               'DSC[CourseID]': 1,  # SCY by default for NCAA meets
               'Gender': gender,
               'Age': age,          # Age doesn't matter in NCAA meets, just give them a standard
               'Minutes': minutes,
               'Seconds': seconds_split[0],
               'Milliseconds': seconds_split[1],
               'divId': 'Times_PowerPointCalculator_Index_Div_1'
               }

    return requests.post(url, data=payload).text


def mcsl_lineup_to_string(lineup):
    pass


# Takes a lineup as input and returns a printable string
def lineup_to_string(lineup, cfg):
    rString = ""
    for swimmer in lineup.keys():
        rString += swimmer + ":\n"
        for event in lineup[swimmer]:
            rString += cfg["EventNames"][str(event[0])] + "\n"
    return rString


def mcsl_score_meet(lineup_one, lineup_two):
    pass


# Takes two optimized lineups and scores the meet between them, returning a dict with names as keys and scores as values
def score_meet(lineup_one, lineup_two):
    pass


def main():

    start = time.time()
    print(swimulate("University_of_Pennsylvania_21_races.jl", "Yale_University_21_races.jl", "F"))

    execution_time = time.time() - start
    print("Execution time: " + str(execution_time))


if __name__ == "__main__":
    main()
