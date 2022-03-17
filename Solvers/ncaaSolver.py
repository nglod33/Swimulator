import numpy as np
import solverUtilities as su
import json

OPPONENT_PP = []
TEAM_PP = []
cfg = json.load(open("configs/NCAA.json"))


# NCAA duel meets are a bit easier to optimize since they value winning so much
# This just optimizes a roster for individual swims. Dives and relays are done separately
def ncaa_duel_optimize(roster_one, roster_two):
    team_one_lineup, team_one_times = su.create_np_array(roster_one, cfg)

    # Find the best non-certain times in the array, and arrange them in order of power points
    i = 0
    j = 0
    pp_coord_list = []
    # First digit: pp score, second two digits: coords
    while i < cfg["RowNumber"]:
        j = 0
        while j < team_one_times.shape[1]:
            if team_one_lineup[i, j] == 0 and team_one_times[i, j] != 0:
                pp_coord_list.append([team_one_times[i, j], i, j])
            j += 1
        i += 1
    # sort the remaining uncategorized times by highest first
    pp_coord_list = sorted(pp_coord_list, key=lambda x: x[0])

    # Set Global vars to team pp and opponent pp because those shouldn't change
    team_two_roster, team_two_times = su.create_np_array(roster_two, cfg)
    global OPPONENT_PP
    OPPONENT_PP = team_two_times
    global TEAM_PP
    TEAM_PP = team_one_times
    lineup, eval_score = su.backtrack_roster(team_one_lineup, pp_coord_list, ncaa_evaluate_lineup)

    # Convert the lineup back to a dict with events as the key and then name-time pairs as the values
    final_lineup_dict = {}
    for index, swimmer in enumerate(roster_one.keys()):
        i = 0
        while i < cfg["RowNumber"]:
            if lineup[i, index] == 0:
                pass
            elif swimmer in final_lineup_dict.keys():
                final_lineup_dict[swimmer].append((i, lineup[i, index]))
            else:
                final_lineup_dict[swimmer] = [(i, lineup[i, index])]
            i += 1

    # Return the finished dict of lineups
    return final_lineup_dict


# Returns integer based on the difference in pp between top 3 swimmers and opponents top n
def ncaa_evaluate_lineup(lineup, n=5):

    # First, calculate the power points
    power_points = np.multiply(lineup, TEAM_PP)

    # Then calculate swim value by using Power Points/(by the number of swimmers on both teams that beat you + 1)
    # TODO: Calculate points based on point scoring
    i = 0
    while i < cfg["RowNumber"]:
        j = 0
        combined_swimmers_best = np.sort(np.append(OPPONENT_PP[i], TEAM_PP[i]))[::-1]
        while j < power_points[i].size:
            if power_points[i, j] != 0:
                # go through the combined swimmers in each event until one beats you
                # Use >= because your own time will always be in there, so at least one person will be >=
                power_points[i, j] = power_points[i, j] // combined_swimmers_best[np.where(combined_swimmers_best >= power_points[i, j])].size
            j += 1
        i += 1

    return lineup, np.sum(power_points)


def main():
    pass


if __name__ == "__main__":
    main()
