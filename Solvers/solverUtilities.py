import numpy as np


# In the MCSL version, this will be used on individual age/gender groups
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


# Find the optimal roster through backtracking. Use evaluate roster to evaluate
# This operates on the assumption that it is always better to have more swimmers in an event.
# There will never be a situation where 2/3 swimmers in an event will be better that 3/3 swimmesr in an event
def backtrack_roster(roster_array, times_list, eval_function):
    # If there are no more choice to make, return the completed roster
    if len(times_list) <= 0:
        return eval_function(roster_array)

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