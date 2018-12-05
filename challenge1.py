""" Advent Of Code Day 1 """

from itertools import accumulate, cycle
from common.input_file import read_numbers


def get_sum_of_frequencies(numbers):
    """
        Given a list of frequencies (positive and negative)
        What is the ending frequency when added together
    """
    return sum(numbers)


def get_first_frequency_listed_twice(numbers):
    """
        Given a list of frequencies (positive and negative)
        What is the first cumulative frequency seen twice
    """
    seen_so_far = set([0])
    for running_total in accumulate(cycle(numbers)):

        if running_total in seen_so_far:
            return running_total

        seen_so_far.add(running_total)

    raise RuntimeError("This code is unreachable")


NUMBERS = read_numbers("input/input1.txt")

if __name__ == "__main__":
    print(get_sum_of_frequencies(NUMBERS))
    print(get_first_frequency_listed_twice(NUMBERS))
