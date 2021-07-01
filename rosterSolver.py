import numpy as np


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
    return


# Returns integer based on the total number of swimmers on the other team beaten
def ncaa_evaluate_lineup(lineup, opposition_lineup):
    return


def main():
    pass


if __name__ == "__main__":
    main()
