"""
    Advent of Code Day 8
"""
from itertools import cycle
from common.input_file import read_single_line

class Player:
    """
        A player representing a score and a number
    """
    def __init__(self, number):
        """
            Constructor
        """
        self.score = 0
        self.number = number

    def add_marble(self, marble):
        """
            Add a marble's score
        """
        self.score += marble.number

    def __str__(self):
        return f"Player: {self.number}   Score: {self.score}"

class Marble:
    """
        Functions as a circular doubly linked list
    """
    def __init__(self, number, next_link=None, prev_link=None):
        """
           Constructor
        """
        self.next = next_link
        self.prev = prev_link
        self.number = number

    def add_marble_after(self, next_number):
        """
            Add a marble immediately after the current one
        """
        next_marble = Marble(next_number, self.next, self)
        self.next.prev = next_marble
        self.next = next_marble
        return next_marble

    def remove(self):
        """
            Remove a Marble
        """
        self.prev.next = self.next
        self.next.prev = self.prev

    def __sub__(self, marbles_away):
        """
            Get the marble `marbles_away` in the counter clockwise direction
        """
        marble = self
        for _ in range(marbles_away):
            marble = marble.prev
        return marble

def create_initial_marble():
    """
        Create the initial marble
    """
    current_marble = Marble(0)
    current_marble.next = current_marble
    current_marble.prev = current_marble
    return current_marble

def get_highest_score(number_of_players, last_marble):
    """
        Get the highest score of a player
    """
    current_marble = create_initial_marble()
    players = [Player(i) for i in range(number_of_players)]
    for marble_number, player in zip(range(1, last_marble + 1), cycle(players)):
        if marble_number % 23 == 0:
            marble_to_remove = current_marble - 7
            current_marble = marble_to_remove.next
            player.add_marble(Marble(marble_number))
            player.add_marble(marble_to_remove)
            marble_to_remove.remove()
        else:
            current_marble = current_marble.next.add_marble_after(marble_number)

    return max(p.score for p in players)

TEXT = read_single_line("input/input9.txt").split()
NUM_PLAYERS, LAST_MARBLE = int(TEXT[0]), int(TEXT[6])
if __name__ == "__main__":
    print(get_highest_score(NUM_PLAYERS, LAST_MARBLE))
    print(get_highest_score(NUM_PLAYERS, LAST_MARBLE*100))
