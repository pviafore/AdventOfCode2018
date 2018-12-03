
def test_day1():
    from challenge1 import NUMBERS, get_sum_of_frequencies, get_first_frequency_listed_twice
    assert get_sum_of_frequencies(NUMBERS) == 442
    assert get_first_frequency_listed_twice(NUMBERS) == 59908

def test_day2():
    from challenge2 import BOX_IDS, get_checksum, get_common_letters_from_correct_boxes
    assert get_checksum(BOX_IDS) == 7936
    assert get_common_letters_from_correct_boxes(BOX_IDS) == "lnfqdscwjyteorambzuchrgpx"

def test_day3():
    from challenge3 import (CLAIMS,
                            CLAIMED_SQUARES,
                            get_number_of_overlapping_squares,
                            get_non_overlapping_claim)
    assert get_number_of_overlapping_squares(CLAIMED_SQUARES) == 98005
    assert get_non_overlapping_claim(CLAIMS, CLAIMED_SQUARES) == "#331 "
