"""
    Advent of Code Day 4
"""
from collections import abc, Counter
import datetime as dt
import re

from common.input_file import get_transformed_input

# man I want a tagged union or ADT for this
def get_action(text):
    """
        Given a list of strings, determin if we are sleeping, awake, or beginning a shift
    """
    if "asleep" in text:
        return Record.SLEEPS
    if "wakes" in text:
        return Record.WAKES
    return Record.BEGINS_SHIFT


def get_id(text):
    """
        Return the guard number if in text else None
    """
    # I also want an optional type
    return text[2] if "Guard" in text else None


class Record:
    """
        A class that represents a specific record from the input
    """

    WAKES = "wakes"
    BEGINS_SHIFT = "begins shift"
    SLEEPS = "sleeps"

    def __init__(self, record):
        """
            Constructor -> takes a string in the format [yyyy-mm-dd hh:mm] <Action>
        """
        _blank, year, month, day, hour, minute, * \
            text = re.split(r"\[|\]|\s|-|\:", record)
        assert year == "1518"
        self.date = dt.datetime(int(year), int(
            month), int(day), int(hour), int(minute))
        self.action = get_action(text)
        self.guard_id = get_id(text)

    def __lt__(self, rhs):
        """
            Less than comparison method
        """
        if self.date > rhs.date:
            return False
        if self.date < rhs.date:
            return True

        return self.guard_id is None and rhs.guard_id is not None

    def __str__(self):
        return f"{self.date} -> {self.action} ID={self.guard_id}"

def date_range_by_minute(begin_date, end_date):
    """
    Give a range of datetimes by the minute
    """
    current_date = begin_date
    while current_date != end_date:
        yield current_date
        current_date += dt.timedelta(minutes=1)


class Guard:
    """
        Represents a single guard and all the times they slept
    """
    def __init__(self, guard_id):
        """Constructor with an ID in the form of #ID"""
        self.guard_id = int(guard_id[1:])
        self.times_slept = []
        self.minutes_slept_frequency = Counter()

    def record_minutes_slept(self, begin_sleep_time, end_sleep_time):
        """
        Record the minutes slept (given two date times)
        """

        date_range = list(date_range_by_minute(begin_sleep_time, end_sleep_time))
        self.times_slept += date_range
        self.minutes_slept_frequency.update(d.minute for d in date_range if d.hour == 0)

    def get_total_minutes_slept(self):
        """
        Return the total minutes recorded as sleeping
        """
        return len(self.times_slept)

    def get_most_likely_minute_to_sleep(self):
        """
        Return the minute the guard is most likely to sleep during
        """
        print(self.minutes_slept_frequency)
        return self.minutes_slept_frequency.most_common(1)[0][0]

    def get_frequency_of_most_likely_minute_to_sleep(self):
        """
        Return how many times the guard slept during the most likely minute
        """
        return self.minutes_slept_frequency.most_common(1)[0][1]

    def does_fall_asleep(self):
        """
        Return if the guard ever falls asleep
        """
        return self.times_slept != []

    def matches_id(self, guard_id):
        """
        Return if the ID matches the guard ID
        """
        return self.guard_id == int(guard_id[1:])

class GuardLog(abc.Iterable):
    """
        An iterable guard log
    """
    def __init__(self):
        self.log = []

    def get_guard(self, guard_id):
        """
        Get the guard.  Any new guard is automatically given a new entry in the log
        """
        if any(guard.matches_id(guard_id) for guard in self.log):
            return next(g for g in self.log if g.matches_id(guard_id))
        self.log.append(Guard(guard_id))
        return self.log[-1]

    def __iter__(self):
        return iter(self.log)


def get_guard_log(records):
    """
    Create a Guard Log - a list of guards
    """
    guards = GuardLog()
    records = iter(records)
    try:
        record = next(records)
        while True:
            assert record.action == Record.BEGINS_SHIFT
            guard = guards.get_guard(record.guard_id)

            record = next(records)
            while record.action != Record.BEGINS_SHIFT:
                assert record.action == Record.SLEEPS
                end = next(records)

                assert end.action == record.WAKES
                guard.record_minutes_slept(record.date, end.date)
                record = next(records)

    except StopIteration:
        pass
    return guards


def get_most_likely_to_sleep_guard_strategy_1(guards):
    """
    Strategy 1 - ID of guard with most minutes slept * most likely minute to sleep
    """
    guard = max(guards, key=Guard.get_total_minutes_slept)
    return guard.guard_id * guard.get_most_likely_minute_to_sleep()


def get_most_likely_to_sleep_guard_strategy_2(guards):
    """
    Strategy 2 - ID of guard with most consistent_sleeping_minute * most likely minute to sleep
    """
    # find the guard with the highest most_likely_minute occuring
    sleepers = [guard for guard in guards if guard.does_fall_asleep()]
    guard = max(sleepers, key=Guard.get_frequency_of_most_likely_minute_to_sleep)
    return guard.guard_id * guard.get_most_likely_minute_to_sleep()


RECORDS = sorted(get_transformed_input("input/input4.txt", Record))
GUARDS = get_guard_log(RECORDS)
if __name__ == "__main__":
    print(get_most_likely_to_sleep_guard_strategy_1(GUARDS))
    print(get_most_likely_to_sleep_guard_strategy_2(GUARDS))
