
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

def test_day4():
    from challenge4 import (GUARDS,
                            get_most_likely_to_sleep_guard_strategy_1,
                            get_most_likely_to_sleep_guard_strategy_2)
    assert get_most_likely_to_sleep_guard_strategy_1(GUARDS) == 95199
    assert get_most_likely_to_sleep_guard_strategy_2(GUARDS) == 7887

def test_day5():
    from challenge5 import POLYMER, get_reduced_polymer_length, get_optimized_polymer_length
    assert get_reduced_polymer_length(POLYMER) == 9562
    assert get_optimized_polymer_length(POLYMER) == 4934

def test_day6():
    from challenge6 import POINTS, get_largest_finite_region, get_safest_finite_region
    assert get_largest_finite_region(POINTS) == 3989
    assert get_safest_finite_region(POINTS) == 49715

def test_day7():
    from challenge7 import STEPS, get_topologically_sorted_steps, get_total_time_needed
    assert get_topologically_sorted_steps(STEPS) == "CQSWKZFJONPBEUMXADLYIGVRHT"
    assert get_total_time_needed("CQSWKZFJONPBEUMXADLYIGVRHT", STEPS, 5) == 914

def test_day8():
    from challenge8 import TREE 
    assert TREE.get_metadata_sum() == 40036
    assert TREE.get_value() == 21677

def test_day9():
    from challenge9 import get_highest_score 
    assert get_highest_score(418, 70769) == 402398
    assert get_highest_score(418, 70769*100) == 3426843186

def test_day12():
    from challenge12 import get_plants_sum, INFO
    assert get_plants_sum(INFO, 20) == 2040
    assert get_plants_sum(INFO, 1_700_000_011)

def test_day13():
    from challenge13 import TRACKS, get_first_crash, get_last_cart_remaining
    assert get_first_crash(TRACKS) == (45, 34)
    assert get_last_cart_remaining(TRACKS) == (91, 25) 