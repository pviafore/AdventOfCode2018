"""
    Advent of Code day 5
"""
from common.input_file import read_single_line

def are_units_reactive(unit1, unit2):
    """
        Return if two units are reactive to one another
        like aA or Aa (not aa or AA)
    """
    return unit1.lower() == unit2.lower() and unit1 != unit2

def get_reduced_polymer_length(polymer):
    """
        Get the polymer length after all reactions have taken place
    """
    stack = []
    for letter in polymer:
        if not stack:
            stack.append(letter)
            continue

        if are_units_reactive(letter, stack[-1]):
            stack.pop()
        else:
            stack.append(letter)

    return len(stack)

def get_optimized_polymer_length(polymer):
    """
        Find the shortest reduced polymer if we were to remove all of one unit (such as A/a)
    """
    lowercase_units = set(l.lower() for l in polymer)
    return min(get_length_after_unit_removal(l, polymer) for l in set(lowercase_units))

def get_length_after_unit_removal(letter, polymer):
    """
        Remove all captial and lowercase versions of the letter
        and returns the reduced length of the polymer
    """
    candidate_polymer = polymer.replace(letter.lower(), "").replace(letter.upper(), "")
    return get_reduced_polymer_length(candidate_polymer)



POLYMER = read_single_line("input/input5.txt")
if __name__ == "__main__":
    print(get_reduced_polymer_length(POLYMER))
    print(get_optimized_polymer_length(POLYMER))
