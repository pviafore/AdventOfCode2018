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
        What is the first frequency listed twice
    """
    seen_so_far = set([0])
    for running_total in accumulate(cycle(numbers)):

        if running_total in seen_so_far:
            return running_total

        seen_so_far.add(running_total)

    raise RuntimeError("This code is unreachable")



INPUT = read_numbers("input1.txt")
print(get_sum_of_frequencies(INPUT))
print(get_first_frequency_listed_twice(INPUT))
