"""
    Advent of Code Day 14
"""

def get_after_improvement_point(point):
    """
        Get the 10 elements after our recipes exceed our improvement point
    """
    elf1_index = 0
    elf2_index = 1
    recipes = "37"
    while len(recipes) <= point + 10:
        elf1_recipe, elf2_recipe = int(recipes[elf1_index]), int(recipes[elf2_index])
        next_recipes = str(elf1_recipe + elf2_recipe)
        recipes += next_recipes
        elf1_index = (elf1_index + elf1_recipe + 1) % len(recipes)
        elf2_index = (elf2_index + elf2_recipe + 1) % len(recipes)

    return recipes[point:point + 10]

def get_recipes_before_improvement_point(point):
    """
        Get the recipes beofre the improvement point in the recipes
    """
    elf1_index = 0
    elf2_index = 1
    recipes = "37"
    while str(point) not in recipes[-12:]:
        elf1_recipe, elf2_recipe = int(recipes[elf1_index]), int(recipes[elf2_index])
        next_recipes = str(elf1_recipe + elf2_recipe)
        recipes += next_recipes
        elf1_index = (elf1_index + elf1_recipe + 1) % len(recipes)
        elf2_index = (elf2_index + elf2_recipe + 1) % len(recipes)

    return recipes.find(str(point))

IMPROVEMENT_POINT = 702831
if __name__ == "__main__":
    print(get_after_improvement_point(IMPROVEMENT_POINT))
    print(get_recipes_before_improvement_point(IMPROVEMENT_POINT))
