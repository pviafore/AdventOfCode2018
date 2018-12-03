"""
   Advent of Code 2018 Day 3
"""
from itertools import product, chain, groupby
import re

from common.input_file import get_transformed_input

def get_claim(claim):
    """
        Transform a claim to an ID and a list of points
    """
    claim_id, left, top, width, height = re.split(r"@|,|:|x", claim)
    left, top, width, height = int(left), int(top), int(width), int(height)
    points = product(range(left, left + width), range(top, top + height))
    return (claim_id, list(points))

def get_claimed_squares(claims):
    """
        Return a dictionary of all claimed squares where key is the coordinate
        and the value is the number of claims
    """
    all_points =  chain.from_iterable(points for _, points in claims)
    rearranged_points = groupby(sorted(all_points))
    return {point: len(list(claims)) for point, claims in rearranged_points}

def get_number_of_overlapping_squares(claimed_squares):
    """
        Get the number of overlapping squares
    """
    return (len([_ for _, claims in claimed_squares.items() if claims > 1]))

def get_non_overlapping_claim(claims, claimed_squares):
    """
        Get the only claim that is not overlapping
    """
    
    def is_unclaimed(points):
        return all(claimed_squares[point] == 1 for point in points)

    try:
        return next(claim_id for claim_id,points in claims if is_unclaimed(points)) 
    except:
        assert False, "We should never hit this line, as this means we didn't find an answer"

CLAIMS = get_transformed_input("input/input3.txt", get_claim)
CLAIMED_SQUARES = get_claimed_squares(CLAIMS)

if __name__ == "__main__":
    print(get_number_of_overlapping_squares(CLAIMED_SQUARES))
    print(get_non_overlapping_claim(CLAIMS, CLAIMED_SQUARES))