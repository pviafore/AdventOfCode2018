"""
    Advent of Code day 21
"""
from typing import Iterable, Set

def get_halting_numbers() -> Iterable[int]:
    """
        Get a list of halting numbers
        Derived this from the assembly
    """
    seen: Set[int] = set()
    d_reg = 65536
    e_reg = 4332021
    while True:
        e_reg += (d_reg & 255)
        e_reg *= 65899
        e_reg = e_reg & 0xFFFFFF
        if d_reg < 256 :
            if e_reg in seen:
                break
            seen.add(e_reg)
            yield e_reg
            d_reg = e_reg | 65536
            e_reg = 4332021
        else:
            d_reg = d_reg // 256

HALTING_NUMBERS = list(get_halting_numbers())

if __name__ == "__main__":
    print(HALTING_NUMBERS[0], HALTING_NUMBERS[-1])

