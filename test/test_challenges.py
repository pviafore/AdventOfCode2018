
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

def test_day14():
    from challenge14 import (IMPROVEMENT_POINT,
                             get_after_improvement_point,
                             get_recipes_before_improvement_point)
    assert get_after_improvement_point(IMPROVEMENT_POINT) == "1132413111"
    assert get_recipes_before_improvement_point(IMPROVEMENT_POINT) == 20340232

def test_day16():
    from challenge16 import (SAMPLES,
                             PROGRAM,
                             get_samples_matching_three_or_more,
                             get_program_results)
    assert get_samples_matching_three_or_more(SAMPLES) == 493
    assert get_program_results(SAMPLES, PROGRAM) == 445

def test_day17():
    from challenge17 import GRID
    assert GRID.get_number_of_tiles_at_rest() == 22474
    assert GRID.get_number_of_tiles_water_reached() == 27736

def test_day18():
    from challenge18 import GRID, transform_over_time, get_total_resource_value
    transform_over_time(GRID, 10)
    assert(get_total_resource_value(GRID) == 384416)

def test_day19():
    from challenge19 import get_actual_value
    assert get_actual_value(875) == 1248
    assert get_actual_value(10551275) == 14952912

def test_day20():
    from challenge20 import CAVE
    assert CAVE.get_max_distance() == 3721
    assert CAVE.get_number_of_rooms_at_least_distance_away(1000) == 8613

def test_day21():
    from challenge21 import HALTING_NUMBERS
    assert HALTING_NUMBERS[0] == 9566170
    assert HALTING_NUMBERS[-1] == 13192622
    