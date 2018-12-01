"""
    A collection of methods to parse input files for Advent of Code puzzles
"""


def read_numbers(input_filename):
    """
        Read a file and return a list of numbers
    """
    with open(input_filename) as input_file:
        return [int(n) for n in input_file.readlines()]
