"""
    Advent of Code Day 13
"""

from itertools import cycle
from common.input_file import read_strings
from common.grid import Point, to_left, to_right, to_below, to_above

class Cart:
    """
        A representation of a cart (position and direction facing)
    """
    def __init__(self, character, position):
        self.position = position
        self.character = character
        self.directions = cycle(["left", "straight", "right"])

    def __str__(self):
        return f"{self.character} {self.position}"

    def move_to_next_position(self):
        """
            moves the cart to the next position
        """
        position_mapping = {
            "v": to_below,
            "^": to_above,
            "<": to_left,
            ">": to_right
        }
        self.position = position_mapping[self.character](self.position)

    def turn_cart_if_needed(self, character):
        """
            If the character is an intersection or bend, turn the cart appropriately
        """
        turn_mapping = {"<": "<", "^": "^", "v": "v", ">": ">"}
        if character == '+':
            direction = next(self.directions)
            if direction == 'left':
                turn_mapping = {"<": "v", "v": ">", ">": "^", "^": "<"}
            if direction == 'right':
                turn_mapping = {"<": "^", "v": "<", ">": "v", "^": ">"}
        if character == '/':
            turn_mapping = {"<": "v", "v": "<", "^": ">", ">": "^"}
        if character == '\\':
            turn_mapping = {"<": "^", "v": ">", "^": "<", ">": "v"}
        self.character = turn_mapping[self.character]


class TrackTimeline:
    """
        A representation of all of our tracks (carts will not be shown on these tracks)
    """
    def __init__(self, tracks, carts):
        self.tracks = tracks
        self.carts = carts
        self.crashes = []


    def __str__(self):
        return "\n".join(t for t in self.tracks)

    def tick(self):
        """
            Run a tick by moving all carts and detecting any crashes
        """
        for cart in self.carts:
            if cart.position in self.crashes:
                continue
            cart.move_to_next_position()
            if any(c.position == cart.position for c in self.carts if c != cart):
                self.crashes.append(cart.position)
            cart.turn_cart_if_needed(self.tracks[cart.position.y][cart.position.x])
        self.carts = sorted(self.carts, key=lambda t: (t.position.y, t.position.x))

    def remove_crashed_carts(self):
        """
            Remove crashed carts from the track
        """
        self.carts = [c for c in self.carts if c.position not in self.crashes]
        self.crashes = []

    def has_crashed(self):
        """
            Return if any cart has crashed
        """
        return self.crashes != []

    def get_crashes(self):
        """
            Get a list of crashes
        """
        return self.crashes

    def get_carts_remaining(self):
        """
            Get the remainng carts
        """
        return self.carts

def is_cart(symbol):
    """
        If the symbol is a cart
    """
    return symbol in ['<', '^', 'v', '>']

def get_carts(tracks):
    """
        A generator for all the positions and direction of carts
    """
    for y_pos, row in enumerate(tracks):
        yield from (Cart(s, Point(x, y_pos)) for x, s in enumerate(row) if is_cart(s))

def get_first_crash(tracks):
    """
        Get the first crash that happened
    """
    carts = list(get_carts(tracks))
    timeline = TrackTimeline(remove_carts_from_track(tracks), carts)
    while not timeline.has_crashed():
        timeline.tick()

    return timeline.get_crashes()[0]

def get_last_cart_remaining(tracks):
    """
        Get the last cart remaining
    """
    carts = list(get_carts(tracks))
    timeline = TrackTimeline(remove_carts_from_track(tracks), carts)
    while len(timeline.get_carts_remaining()) != 1:
        timeline.tick()
        timeline.remove_crashed_carts()

    return timeline.get_carts_remaining()[0].position

def get_underlying_track(symbol):
    """
        Get the track that is under the cart
    """
    return symbol.replace("<", "-").replace(">", "-").replace("v", "|").replace("^", "|")

def remove_carts_from_track(tracks):
    """
        Remove all the carts from the track
    """
    return [get_underlying_track(t) for t in tracks]

TRACKS = read_strings("input/input13.txt")
if __name__ == "__main__":
    print(get_first_crash(TRACKS))
    print(get_last_cart_remaining(TRACKS))
