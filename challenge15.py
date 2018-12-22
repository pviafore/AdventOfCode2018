"""
    Advent of Code Day 15
"""
from itertools import chain, count
from typing import List

from common.grid import TextGrid, get_orthogonally_adjacent, Point
from common.input_file import read_strings

def is_player(_, character: str) -> bool:
    """
        Check if we are an elf or goblin
    """
    return character in ["E", "G"]

def get_opposing_player(player: str)-> str:
    """
        Get the opposing player
    """
    return "G" if player == "E" else "E"

def sort_by_reading_order(seq):
    """
        Sort by reading order (the first element must be a point)
    """
    return sorted(seq, key=lambda p: (p[0].y, p[0].x))


class Battlefield:
    """
        A battlefield class that tracks game state
    """
    def __init__(self, cave, elf_attack_power=3, stop_on_elf_death=False):
        self.cave = TextGrid(cave, "#")
        self.health = {p: 200 for p, _ in self.cave.get_characters(lambda _, v: v in "EG")}
        self.elf_attack_power = elf_attack_power
        self.stop_on_elf_death = stop_on_elf_death
        self.dead = []

    def __str__(self):
        return str(self.cave)

    def is_any_side_defeated(self) -> bool:
        """
            Return if one side is defeated
        """
        return self.cave.get_characters("E") == [] or self.cave.get_characters("G") == []

    def did_all_elves_survive(self) -> bool:
        """
            Did all the elves survive
        """
        return "E" not in self.dead

    def get_attack_power(self, player: str) -> int:
        """
            Return 3 if its a goblin and elf attack otherwise
        """
        return 3 if player == "G" else self.elf_attack_power

    def battle(self):
        """
            Continue rounds of combat (move and attack)
            until one side is defeated
            (or if the first elf dies and stop on first elf death is true)
        """
        for round_number in count(1):
            players = sort_by_reading_order(self.cave.get_characters(is_player))
            for position, player in players:
                if self.is_any_side_defeated():
                    return (round_number -1) * sum(self.health.values())
                # make sure the player has not died
                if self.cave[position] != player:
                    continue
                opposing_player = get_opposing_player(player)
                targets = self.get_targets(opposing_player)
                if targets and not self.cave.is_adjacent_to(position, opposing_player):
                    position = self.move_player(position, targets)
                if self.cave.is_adjacent_to(position, opposing_player):
                    self.attack_player(position)
                    if self.stop_on_elf_death and "E" in self.dead:
                        return (round_number - 1) * sum(self.health.values())
        raise RuntimeError("Unreachable code")

    def attack_player(self, position: Point):
        """
            Find the target with lowest health points and attack it
            If it's dead, remove it
        """
        opposing_player = get_opposing_player(self.cave[position])
        target = self.get_target(position, opposing_player)
        self.health[target] -= self.get_attack_power(self.cave[position])
        self.remove_if_dead(target)

    def remove_if_dead(self, target: Point):
        """
            Remove a character is dead
        """
        if self.health[target] < 0:
            del self.health[target]
            self.dead.append(self.cave[target])
            self.cave[target] = "."

    def move_player(self, position: Point, targets: List[Point]):
        """
            Move a player to the closest target
        """
        targets = self.cave.get_closest_targets(position, targets, "EG#")
        if not targets:
            return position

        last, length = sort_by_reading_order(targets)[0]
        next_step = self.cave.get_best_next_step(position, last, length, "EG#")
        self.cave.move(position, next_step, ".")
        self.health[next_step] = self.health[position]
        del self.health[position]
        return next_step

    def get_targets(self, desired: str) -> List[Point]:
        """
            Get a list of targets adjacent to an enemy
        """
        orthogonal = [get_orthogonally_adjacent(p) for p, _ in self.cave.get_characters(desired)]
        unique = list(set(chain.from_iterable(orthogonal)))
        return [p for p in unique if self.cave[p] == "."]

    def get_target(self, point: Point, desired: str):
        """
            Get the best target (check lowest HP, then reading order)
        """
        potential = [p for p in get_orthogonally_adjacent(point) if self.cave[p] == desired]
        if not potential:
            return None
        min_hp = min(self.health[p] for p in potential)
        return next(p for p in potential if self.health[p] == min_hp)

def get_lowest_outcome_where_no_elves_die(cave):
    """
        Get the first outcome (with lowest attack power) where no elves die
    """
    for elf_attack_power in count(4):
        battlefield = Battlefield(cave, elf_attack_power, stop_on_elf_death=True)
        answer = battlefield.battle()
        if battlefield.did_all_elves_survive():
            return answer
    raise RuntimeError("Unreachable code")


CAVE = read_strings("input/input15.txt")
if __name__ == "__main__":
    print(Battlefield(CAVE).battle())
    print(get_lowest_outcome_where_no_elves_die(CAVE))
