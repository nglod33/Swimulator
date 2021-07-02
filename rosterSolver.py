import numpy as np

# Col of events in the numpy array
EVENTS_DICT = {
    150: 0,
    1100: 1,
    1200: 2,
    1500: 3,
    11000: 4,
    11650: 5,
    2100: 6,
    2200: 7,
    3100: 8,
    3200: 9,
    4100: 10,
    4200: 11,
    5200: 12,
    5400: 13
}

CONSIDERATION_THRESHOLD = 5
EVENT_NUMBER = 14


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


# Takes a team dict and creates an array of power points out of it
def create_np_array(roster_one):

    # Times array shows power scores for times
    # Lineup array shows who's swimming (1 for swimming, 0 for not swimming)
    times_array = np.zeros([EVENT_NUMBER, len(roster_one.keys())])
    lineup_array = np.zeros([EVENT_NUMBER, len(roster_one.keys())])
    for index, swimmer in enumerate(roster_one.values()):
        for event in swimmer.keys():
            lineup_array[EVENTS_DICT[event], index] = swimmer[event]

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
    while i < lineup_array.shape[1]:
        nonzero_count = np.count_nonzero(times_array[:, i])
        # Checks to see if the swimmer has 3 or less events, if yes, it considers them for automatic qualification
        if nonzero_count <= 3:
            j = 0
            while j < EVENT_NUMBER:
                if times_array[i, j] > 0:
                    # Checks to see if the swimmer is top 3 in the event, if yes, automatically puts them in
                    if times_array[i, j] >= np.sort(times_array[i])[::-1][:3][-1]:
                        lineup_array[i, j] = 1
                j += 1
        i += 1

    return lineup_array, times_array


# Returns integer based on the difference in pp between top 3 swimmers and opponents top n
def ncaa_evaluate_lineup(lineup, times, opposition, n=5):
    return


def main():
    pass


if __name__ == "__main__":
    main()
