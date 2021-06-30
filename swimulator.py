import json
import requests

# The inputs are the names of the team jl files
EVENTS_DICT = {
    150: "50 free",
    1100: "100 free",
    1200: "200 free",
    1500: "500 free",
    11000: "1000 free",
    11650: "1650 free",
    2100: "100 back",
    2200: "200 back",
    3100: "100 breast",
    3200: "200 breast",
    4100: "100 fly",
    4200: "200 fly",
    5200: "200 IM",
    5400: "400 IM",
    6200: "200 free relay",
    6400: "400 free relay",
    7800: "800 free relay",
    8200: "200 medley relay",
    8400: "400 medley relay"
}


def swimulate(team1, team2, gender, age=25):
    # Build a dict of swimmers with their names as keys and a dict of race-time pairs as the value
    # Gender needed for power point calculation
    # Age included for future expansion to mcsl
    team_1_dict = create_dict(team1)
    team_2_dict = create_dict(team2)
    return


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


def calculate_lineup(team_dict):
    # First, replace times with power points
    for swimmer in team_dict.values():
        pass
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

    payload = {'DSC[DistanceID]': EVENTS_DICT[event_id].split(' ')[0],
               'DSC[StrokeID]': str(event_id)[0],
               'DSC[CourseID]': 3,  # SCY by default for NCAA meets
               'Gender': gender,
               'Age': age,          # Age doesn't matter in NCAA meets, just give them a standard
               'Minutes': minutes,
               'Seconds': seconds_split[0],
               'Milliseconds': seconds_split[1],
               'divId': 'Times_PowerPointCalculator_Index_Div_1'
               }

    return requests.post(URL, data=payload).text


def main():
    print(calculate_power_points("1:54.01", 2200, "F"))


if __name__ == "__main__":
    main()
