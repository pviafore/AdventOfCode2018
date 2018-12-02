"""
    Advent of Code Day 2
"""
from itertools import groupby, combinations

from common.input_file import read_strings


def transform_input(box_id):
    """
        We sort and groupby to get lists of letters from each ID
    """
    grouped_box_id = groupby(sorted(box_id))

    # We need to convert to a list so that we may go through this
    # list more than once, otherwise we exhaust iterators first time through

    return [(key, list(group)) for key, group in grouped_box_id]

def get_checksum(box_ids):
    """
        Get the checksum of all the box IDs
        Expects the box ids to be grouped and sorted
    """
    grouped_box_ids = [transform_input(box_id) for box_id in box_ids]

    return (
        get_number_of_boxes_with_exact_letters(grouped_box_ids, 2) *
        get_number_of_boxes_with_exact_letters(grouped_box_ids, 3)
        )

def get_number_of_boxes_with_exact_letters(grouped_box_ids, desired_count):
    """
        Gets the count of boxes where we have exactly `desired_count`
        number of one letter in it
    """
    candidates = [True for box in grouped_box_ids if contains_desired_count(box, desired_count)]
    return len(candidates)

def contains_desired_count(box, desired_count):
    """
        If the box has exatly 'desired_count` of any one letter
    """
    return any(group for _, group in box if len(group) == desired_count)

def get_common_letters_from_correct_boxes(box_ids):
    """
        Get the common letters from the correct boxes
    """
    _box1, _box2, common_letters = get_correct_boxes(box_ids)
    return common_letters 

def get_correct_boxes(box_ids):
    """
        Get the pair of correct boxes
    """
    box_pairs = combinations(box_ids, 2)

    # get the common letters for each box so that we can see which ones are only one off
    candidates = [(box1, box2, get_common_letters(box1, box2)) for box1, box2 in box_pairs]
    try:
        return next(candidate for candidate in candidates if is_off_by_one_letter(candidate))
    except StopIteration:
        assert False, "We did not find a suitable answer in the input"

def is_off_by_one_letter(candidate):
    """
        Return true if the boxes are off by one letter
    """
    box1, _, common_letters = candidate
    return len(common_letters) == len(box1) - 1

def get_common_letters(box1, box2):
    """
        Get the letters in common between two boxes
    """
    return "".join([letter1 for letter1, letter2 in zip(box1, box2) if letter1 == letter2])

# We sort and groupby to make it easier to find out how many of each letter there is
BOX_IDS = read_strings("input/input2.txt")
print(get_checksum(BOX_IDS))
print(get_common_letters_from_correct_boxes(BOX_IDS))
