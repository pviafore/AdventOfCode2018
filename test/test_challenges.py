import unittest

class TestChallenges(unittest.TestCase):
    def test_day1(self):
        from challenge1 import NUMBERS, get_sum_of_frequencies, get_first_frequency_listed_twice
        assert get_sum_of_frequencies(NUMBERS) == 442
        assert get_first_frequency_listed_twice(NUMBERS) == 59908

    def test_day2(self):
        from challenge2 import BOX_IDS, get_checksum, get_common_letters_from_correct_boxes
        assert get_checksum(BOX_IDS) == 7936
        assert get_common_letters_from_correct_boxes(BOX_IDS) == "lnfqdscwjyteorambzuchrgpx"
