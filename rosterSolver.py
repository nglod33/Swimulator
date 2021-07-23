import numpy as np

# Col of events in the numpy array
EVENTS_DICT = {
    "150": 0,
    "1100": 1,
    "1200": 2,
    "1500": 3,
    "11000": 4,
    "11650": 5,
    "2100": 6,
    "2200": 7,
    "3100": 8,
    "3200": 9,
    "4100": 10,
    "4200": 11,
    "5200": 12,
    "5400": 13
}

OPPONENT_PP = []
TEAM_PP = []

CONSIDERATION_THRESHOLD = 5
EVENT_NUMBER = 14
EVENTS_PER_SWIMMER = 3
SWIMMERS_PER_EVENT = 3


def optimize(roster_one, roster_two, isNCAA=True):
    if isNCAA:
        return ncaa_duel_optimize(roster_one, roster_two)
    else:
        return mcsl_optimize(roster_one, roster_two)


# TODO: Implement backtracking for MCSL solution after ncaa is complete
def mcsl_optimize(roster_one, roster_two):
    return


# NCAA duel meets are a bit easier to optimize since they value winning so much
# This just optimizes a roster for individual swims. Dives and relays are done separately
def ncaa_duel_optimize(roster_one, roster_two):
    team_one_lineup, team_one_times = create_np_array(roster_one)

    # Find the best non-certain times in the array, and arrange them in order of power points
    i = 0
    j = 0
    pp_coord_list = []
    # First digit: pp score, second two digits: coords
    while i < EVENT_NUMBER:
        j = 0
        while j < team_one_times.shape[1]:
            if team_one_lineup[i, j] == 0 and team_one_times[i, j] != 0:
                pp_coord_list.append([team_one_times[i, j], i, j])
            j += 1
        i += 1
    # sort the remaining uncategorized times by highest first
    pp_coord_list = sorted(pp_coord_list, key=lambda x: x[0])

    # Set Global vars to team pp and opponent pp because those shouldn't change
    team_two_roster, team_two_times = create_np_array(roster_two)
    global OPPONENT_PP
    OPPONENT_PP = team_two_times
    global TEAM_PP
    TEAM_PP = team_one_times
    lineup, eval_score = backtrack_roster(team_one_lineup, pp_coord_list)

    # Convert the lineup back to a dict with events as the key and then name-time pairs as the values
    final_lineup_dict = {}
    for index, swimmer in enumerate(roster_one.keys()):
        i = 0
        while i < EVENT_NUMBER:
            if lineup[i, index] == 0:
                pass
            elif swimmer in final_lineup_dict.keys():
                final_lineup_dict[swimmer].append((i, lineup[i, index]))
            else:
                final_lineup_dict[swimmer] = [(i, lineup[i, index])]
            i += 1

    # Return the finished dict of lineups
    return final_lineup_dict


# Find the optimal roster through backtracking. Use evaluate roster to evaluate
# This operates on the assumption that it is always better to have more swimmers in an event.
# There will never be a situation where 2/3 swimmers in an event will be better that 3/3 swimmesr in an event
def backtrack_roster(roster_array, times_list):
    # If there are no more choice to make, return the completed roster
    if len(times_list) <= 0:
        return ncaa_evaluate_lineup(roster_array)

    next_choice = times_list.pop(0)
    # First, evaluate outcomes if you don't swim this swimmer in this event
    without_next_lineup, without_next_score = backtrack_roster(roster_array, times_list)

    with_next_score = 0
    with_next_pp = 0
    # Check if possible by checking current swimmers for this event, and current events for this swimmer
    if np.sum(roster_array[next_choice[1]]) < SWIMMERS_PER_EVENT \
            and np.sum(roster_array[:, next_choice[2]]) < EVENTS_PER_SWIMMER:
        roster_array[next_choice[1], next_choice[2]] = 1
        with_next_lineup, with_next_score = backtrack_roster(roster_array, times_list)

    # return the result with the greater eval
    if without_next_score > with_next_score:
        return without_next_lineup, without_next_score
    else:
        return with_next_lineup, with_next_score


# Returns integer based on the difference in pp between top 3 swimmers and opponents top n
def ncaa_evaluate_lineup(lineup, n=5):

    # First, calculate the power points
    power_points = np.multiply(lineup, TEAM_PP)

    # Then calculate swim value by using Power Points/(by the number of swimmers on both teams that beat you + 1)
    i = 0
    while i < EVENT_NUMBER:
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


# Takes a team dict and creates an array of power points out of it
def create_np_array(roster_one):

    # Times array shows power scores for times
    # Lineup array shows who's swimming (1 for swimming, 0 for not swimming)
    times_array = np.zeros([EVENT_NUMBER, len(roster_one.keys())])
    lineup_array = np.zeros([EVENT_NUMBER, len(roster_one.keys())])
    for index, swimmer in enumerate(roster_one.values()):
        for event in swimmer.keys():
            times_array[EVENTS_DICT[event], index] = swimmer[event]

    # Sets every time not in the top 5 to zeroes
    i = 0
    while i < EVENT_NUMBER:
        # Sort the list, reverse it, take the first 5 elements, then take the last one of them
        # This makes it so that even if there's less than 5 swimmers it won't throw an error
        time_threshold = np.sort(times_array[i])[::-1][:CONSIDERATION_THRESHOLD][-1]

        # Set all times less than the threshold to 0, do not consider them
        j = 0
        while j < times_array.shape[1]:
            if times_array[i, j] < time_threshold:
                times_array[i, j] = 0
            j += 1
        i += 1

    # If a swimmer is top 3 in an event and not in the top 5 for any other, automatically put them in that event
    # Do this by changing that index in the lineup_array to a 1
    # Once that is done, we can then use that lineup array and times array as a a start point for the tree
    i = 0
    while i < times_array.shape[1]:
        nonzero_count = np.count_nonzero(times_array[:, i])
        # Checks to see if the swimmer has 3 or less events, if yes, it considers them for automatic qualification
        if nonzero_count <= EVENTS_PER_SWIMMER:
            j = 0
            while j < EVENT_NUMBER:
                if times_array[j, i] > 0 and times_array[j][np.where(times_array[j] > times_array[j, i])].size < 3:
                    # Checks to see if the swimmer is top 3 in the event, if yes, automatically puts them in
                    lineup_array[j, i] = 1
                j += 1
        i += 1

    return lineup_array, times_array


def main():
    pass


if __name__ == "__main__":
    main()
