"""
    Advent of Code Day 13
"""

from itertools import cycle
from common.input_file import read_strings
from common.grid import MapGrid, to_left, to_right, to_below, to_above

def remove_cart(symbol):
    """
        get the underlying track under the crt
    """
    return symbol.replace("<", "-").replace(">", "-").replace("v", "|").replace("^", "|")

class Cart:
    """
        A representation of a cart (position and direction facing)
    """
    def __init__(self, symbol, position):
        self.symbol = symbol
        self.position = position
        self.directions = cycle(["left", "straight", "right"])
        self.underlying_track = remove_cart(symbol)

    def move(self):
        """
            moves the cart to the next position
        """
        position_mapping = {
            "v": to_below,
            "^": to_above,
            "<": to_left,
            ">": to_right
        }
        self.position = position_mapping[self.symbol](self.position)

    def turn_cart_if_needed(self):
        """
            If the character is an intersection or bend, turn the cart appropriately
        """
        turn_mapping = {"<": "<", "^": "^", "v": "v", ">": ">"}
        if self.underlying_track == '+':
            direction = next(self.directions)
            if direction == 'left':
                turn_mapping = {"<": "v", "v": ">", ">": "^", "^": "<"}
            if direction == 'right':
                turn_mapping = {"<": "^", "v": "<", ">": "v", "^": ">"}
        if self.underlying_track == '/':
            turn_mapping = {"<": "v", "v": "<", "^": ">", ">": "^"}
        if self.underlying_track == '\\':
            turn_mapping = {"<": "^", "v": ">", "^": "<", ">": "v"}
        self.symbol = turn_mapping[self.symbol]

    def get_underlying_track(self):
        """
            Get the track that is under the cart
        """
        return self.underlying_track


class TrackTimeline:
    """
        A representation of all of our tracks (carts will not be shown on these tracks)
    """
    def __init__(self, tracks):
        self.map = MapGrid(tracks, " ")
        self.carts = [Cart(c, pos) for pos, c in self.map.get_characters(is_cart)]
        self.crashes = []

    def __str__(self):
        return str(self.map)

    def tick(self):
        """
            Run a tick by moving all carts and detecting any crashes
        """
        for cart in self.carts:
            if cart.position in self.crashes:
                continue

            first_position = cart.position
            cart.move()

            old_track = cart.underlying_track
            cart.underlying_track = self.map[cart.position]
            self.map.move(first_position, cart.position, old_track)
            cart.turn_cart_if_needed()
            self.map[cart.position] = cart.symbol

            for other_cart in self.carts:
                if cart.position == other_cart.position and other_cart != cart:
                    self.crashes.append(cart.position)
                    self.map[cart.position] = other_cart.get_underlying_track()

        self.carts = sorted(self.carts, key=lambda c: (c.position.y, c.position.x))

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

def is_cart(_point, symbol):
    """
        If the symbol is a cart
    """
    return symbol in ['<', '^', 'v', '>']

def get_first_crash(tracks):
    """
        Get the first crash that happened
    """
    timeline = TrackTimeline(tracks)
    while not timeline.has_crashed():
        timeline.tick()

    return timeline.get_crashes()[0]

def get_last_cart_remaining(tracks):
    """
        Get the last cart remaining
    """
    timeline = TrackTimeline(tracks)
    while len(timeline.get_carts_remaining()) != 1:
        timeline.tick()
        timeline.remove_crashed_carts()

    return timeline.get_carts_remaining()[0].position

TRACKS = read_strings("input/input13.txt")
if __name__ == "__main__":
    print(get_first_crash(TRACKS))
    print(get_last_cart_remaining(TRACKS))
