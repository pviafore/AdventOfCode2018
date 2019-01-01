"""
    Advent of Code Day 24
"""
from itertools import count
import re
from typing import List
from common.input_file import read_strings

class Army:
    """
        A grouping of related units
    """
    def __init__(self, units, hit_points, initiative):
        self.units = units
        self.hit_points = hit_points
        self.initiative = initiative
        self.immunities = []
        self.weaknesses = []
        self.attack = 0
        self.attack_type = ""

    def set_immunities_and_weaknesses(self, immunities: List[str], weaknesses: List[str]):
        """
            Set the immunities and weaknesses
        """
        self.immunities = immunities
        self.weaknesses = weaknesses

    def set_attack(self, attack: int, attack_type: str):
        """
            Set the attack and attack type
        """
        self.attack = attack
        self.attack_type = attack_type

    def __str__(self):
        return (f"{self.units} @ {self.hit_points}\n" +
                f"Immunities: {', '.join(self.immunities)}\n" +
                f"Weaknesses: {', '.join(self.weaknesses)}\n" +
                f"Attack: {self.attack_type} {self.attack}    Initiative: {self.initiative}")

    def get_effective_power(self):
        """
            Get the units multiplied by the attack
        """
        return self.units * self.attack

    def take_damage(self, damage: int):
        """
            Take damage and remove units
        """
        total_health = self.hit_points * self.units
        total_health -= damage
        self.units = total_health // self.hit_points
        if total_health % self.hit_points != 0:
            self.units += 1

    def is_alive(self) -> bool:
        """
            Are there any units left?
        """
        return self.units > 0


def get_weaknesses(weaknesses_and_immunities: str) -> List[str]:
    """
        Get the weaknesses from the string inside the parentheses
    """
    match = re.search(r"weak to ((?:\w*[, ]?)+)", weaknesses_and_immunities)
    return [] if match is None else match.group(1).split(", ")

def get_immunities(weaknesses_and_immunities: str) -> List[str]:
    """
        Get the immunities from the string inside the parentheses
    """
    match = re.search(r"immune to ((?:\w*[, ]?)+)", weaknesses_and_immunities)
    return [] if match is None else match.group(1).split(", ")

def to_army(army_str: str) -> Army:
    """
        Convert the string to an Army
    """
    match = re.match(r"(\d+) units each with (\d+) hit points (?:\(([^\)]*)\) )?"+
                     r"with an attack that does (\d+) (\w+) damage at initiative (\d+)", army_str)
    assert match is not None, army_str
    groups = match.groups()
    army = Army(int(groups[0]), int(groups[1]), int(groups[-1]))

    weaknesses = get_weaknesses(groups[2]) if groups[2] is not None else []
    immunities = get_immunities(groups[2]) if groups[2] is not None else []

    army.set_immunities_and_weaknesses(immunities, weaknesses)
    army.set_attack(int(groups[-3]), groups[-2])
    return army

def parse_immune_and_infection(armies: List[str]):
    """
        Parse out immune and infection groups
    """
    seperator = armies.index("")
    return list(map(to_army, armies[1:seperator])), list(map(to_army, armies[seperator+2:]))

def process_round(immune_system, infection):
    """
        Process a single round
    """
    targets = get_targets(immune_system, infection)
    for attacker, defender in sorted(targets.items(), key=lambda a: a[0].initiative, reverse=True):
        if attacker.is_alive():
            defender.take_damage(get_damage_dealt(attacker, defender))

def wage_war(immune_system, infection):
    """
        Wage war between the two sides (and return the end results)
    """
    while immune_system and infection:
        original = [a.units for a in immune_system + infection]
        process_round(immune_system, infection)
        immune_system = [i for i in immune_system if i.is_alive()]
        infection = [i for i in infection if i.is_alive()]
        if original == [a.units for a in immune_system + infection]:
            # stalemate
            return immune_system, infection
    return immune_system, infection

def get_units_left(armies: List[Army]) -> int:
    """
        Get the number of armies left
    """
    return sum(army.units for army in armies)

def get_result_of_war(armies):
    """
        Get the result of the war
    """
    immune, infection = parse_immune_and_infection(armies)
    immune, infection = wage_war(immune, infection)
    return get_units_left(immune) if immune else get_units_left(infection)

def get_target_selection_key(army: Army):
    """
        For use in sorted (effective, power, initiative)
    """
    return (army.get_effective_power(), army.initiative)

def get_attack_key(attacker, enemy):
    """
        For use in sorted (damage dealt, enemy effective power, initiative)
    """
    return (get_damage_dealt(attacker, enemy), enemy.get_effective_power(), enemy.initiative)

def get_damage_dealt(attacker: Army, enemy: Army):
    """
        Get the damage dealt from an attacker to an enemy
    """
    base_damage = attacker.get_effective_power()
    assert base_damage > 0
    if attacker.attack_type in enemy.immunities:
        base_damage = 0
    if attacker.attack_type in enemy.weaknesses:
        base_damage *= 2
    return base_damage

def sort_by_attack_key(attacker, armies, already_attacked):
    """
        Sort by attack key and don't include already attacked
    """
    enemies = sorted(armies, key=lambda a: get_attack_key(attacker, a), reverse=True)
    return [e for e in enemies if e not in already_attacked]

def get_targets(immune, infect):
    """
        Get a dictionary of attacker -> defender
    """
    targets = {}

    sorted_immune = sorted(immune, key=get_target_selection_key, reverse=True)
    for immune_system in sorted_immune:
        enemies = sort_by_attack_key(immune_system, infect, targets.values())
        if enemies and get_damage_dealt(immune_system, enemies[0]):
            targets[immune_system] = enemies[0]

    sorted_infect = sorted(infect, key=get_target_selection_key, reverse=True)
    for infector in sorted_infect:
        enemies = sort_by_attack_key(infector, immune, targets.values())
        if enemies and get_damage_dealt(infector, enemies[0]):
            targets[infector] = enemies[0]
    return targets

def get_lowest_boost(armies: List[str]):
    """
        Get the lowest boost for the immune system to work
    """
    immune, infection = parse_immune_and_infection(armies)
    for boost in count(1):
        immune, infection = parse_immune_and_infection(armies)
        for immune_system in immune:
            immune_system.attack += boost
        immune, infection = wage_war(immune, infection)
        if not infection:
            return get_units_left(immune)
    raise RuntimeError("Should not be possible to get here")

ARMIES = read_strings("input/input24.txt")
print(get_result_of_war(ARMIES))
print(get_lowest_boost(ARMIES))
