import json
import requests
import rosterSolver as rs


def swimulate(team1, team2, gender, age=25):
    # Build a dict of swimmers with their names as keys and a dict of race-time pairs as the value
    # Gender needed for power point calculation
    # Age included for future expansion to mcsl
    team_1_dict = create_dict(team1)
    team_2_dict = create_dict(team2)

    team_1_lineup, team_2_lineup = calculate_lineup(team_1_dict, team_2_dict, gender)

    return get_results(team_1_lineup, team_2_lineup)


def create_dict(team):
    return_dict = {}
    with open(team, 'rb') as f:
        for line in f:
            item = dict(json.loads(line))
            if item["name"] in return_dict.keys():
                return_dict[item['name']][item['event']] = item['time']
            else:
                return_dict[item['name']] = {item['event']: item['time']}
    return return_dict


def calculate_lineup(team_dict_one, team_dict_two, gender):

    # First, replace times with power points
    for swimmer in team_dict_one.values():
        for event in swimmer:
            swimmer[event] = calculate_power_points(swimmer[event], event, gender)

    for swimmer in team_dict_two.values():
        for event in swimmer:
            swimmer[event] = calculate_power_points(swimmer[event], event, gender)

    optimized_team_one = rs.optimize(team_dict_one, team_dict_two)
    optimized_team_two = rs.optimize(team_dict_two, team_dict_one)

    return optimized_team_one, optimized_team_two


# Given the optimal lineup of each team, tablulate/display the results
# Add in relays and diving in this stage
# *Shouldn't* need to optimize for diving or relays, just use best scores and times
def get_results(lineup_one, lineup_two):
    return


def calculate_power_points(time, event_id, gender, age=25):
    URL = "https://www.usaswimming.org/api/Times_PowerPointCalculator/CalculatePowerPoints"

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

    return requests.post(URL, data=payload).text


def main():
    team_dict = create_dict('Harvard_University_22_races.jl')
    print(calculate_lineup(team_dict, "F"))


if __name__ == "__main__":
    main()
