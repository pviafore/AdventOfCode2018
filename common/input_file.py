"""
    A collection of methods to parse input files for Advent of Code puzzles
"""
from typing import List

def read_numbers(input_filename: str) -> List[int]:
    """
        Read a file and return a list of numbers
    """
    return get_transformed_input(input_filename, int)

def read_strings(input_filename: str) -> List[str]:
    """
        Read a file and return a list of strings
    """
    return get_transformed_input(input_filename, str)

def get_transformed_input(input_filename: str, transform_function):
    """
        Read all the lines of a file and transform it according to
        transform_function
    """
    with open(input_filename) as input_file:
        return [transform_function(line.rstrip()) for line in input_file]

def read_single_line(input_filename: str, transform_function=str) -> str:
    """
        Read a single line of a file and transform it according to
        transform function
    """
    return get_transformed_input(input_filename, transform_function)[0]
