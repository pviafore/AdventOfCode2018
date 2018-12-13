"""
    Advent of Code Day 12
"""

from common.input_file import read_strings

class PlantRow():
    """
        Make a row of plants
    """
    def __init__(self, state, left_index):
        """
            Initialize a plant row given a state, and the left most index of a plant
        """
        self.state = "...." + state.rstrip(".").lstrip(".") + "...."
        self.left_index = left_index - 4


    def sliding_window(self):
        """
            A generator that gives 5 plants at a time
        """
        for i in range(len(self.state) - 5):
            yield self.state[i:i+5]

    def is_plant(self, index):
        """
            Return if the index is a plant;
        """
        return self.state[index - self.left_index] == "#"

    def get_sum(self):
        """
            Get the sum of the indices that have a plant
        """
        return sum(index for index, p in enumerate(self.state, self.left_index) if p == "#")

    def __str__(self):
        """
            Return a string
        """
        return self.state

    def get_left_most_plant_index(self):
        """
            Get the left most plant index
        """
        return get_left_most_plant_index(self.state, self.left_index)

    def __eq__(self, rhs):
        return self.state == rhs.state

def to_plant_instruction(plant_instruction):
    """
        Converts a triplet to a pair: pattern and result
    """
    return plant_instruction[0], plant_instruction[2]

def get_left_most_plant_index(plant_row, left_index):
    """
        Get the left most plant index
    """
    return next(index for index, plant in enumerate(plant_row, left_index) if plant == "#")


def get_plants_sum(plant_info, num_generations):
    """
        Apply the plant spreading for a number of generations and return the sum
    """
    plants = PlantRow(plant_info[0].split()[2], 0)
    plant_instructions = dict(to_plant_instruction(p.split()) for p in plant_info[2:])
    for generation in range(num_generations):
        old_plants = plants
        new_plants = "".join(plant_instructions.get(p, ".") for p in plants.sliding_window())
        # we add 2 here to account for our padding shenanigans
        plants = PlantRow(new_plants, get_left_most_plant_index(new_plants, plants.left_index + 2))
        if old_plants == plants:
            plants.left_index += (num_generations - generation - 1)
            break
    return plants.get_sum()

INFO = read_strings("input/input12.txt")
if __name__ == "__main__":
    print(get_plants_sum(INFO, 20))
    print(get_plants_sum(INFO, 50_000_000))
