"""
    Advent of Code Day 16
"""

from collections import namedtuple
from typing import Callable, List
from re import split

from common.input_file import read_strings
from common.opcodes import OPCODES

INPUT = read_strings("input/input16.txt")
Sample = namedtuple("Sample", ["before", "opcode", "after"])

def matches(sample, func) -> bool:
    """
        If the sample matches the function
    """
    _, in1, in2, out = sample.opcode
    return func(in1, in2, out, list(sample.before)) == sample.after

def to_opcode(opcode: str) -> List[int]:
    """
        Takes an opcode string and returns a list of four numbers
    """
    return list(map(int, opcode.split()))

def get_samples_and_program(input_data: List[str]):
    """
        Get a list of samples and program
    """
    samples: List[Sample] = []
    while input_data[0].startswith("Before:"):
        line1, opcode, line3, _blank, *input_data = input_data
        # We assume trusted input for these challenges, so we'll eval
        before = [int(b) for b in split(r"Before: \[|, |\]", line1) if b]
        after = [int(a) for a in split(r"After:  \[|, |\]", line3) if a]
        samples.append(Sample(before, to_opcode(opcode), after))
    return samples, [i for i in map(to_opcode, input_data) if i]

SAMPLES, PROGRAM = get_samples_and_program(INPUT)

def get_matches(sample: Sample) -> List[Callable]:
    """
        Get a list of ops that match a sample
    """
    return [op for op in OPCODES if matches(sample, op)]

def get_number_of_matches(sample: Sample) -> int:
    """
        Get a number of matches for a sample
    """
    return len(get_matches(sample))

def get_samples_matching_three_or_more(samples):
    """
        Get the number of samples matching 3 or more opcodes
    """
    return len([sample for sample in samples if get_number_of_matches(sample) >= 3])

def get_opcode_mapping(samples):
    """
        Get the opcode mapping given all the samples
    """
    ops = {num: list(OPCODES) for num in range(16)}
    for sample in samples:
        ops[sample.opcode[0]] = [op for op in ops[sample.opcode[0]] if op in get_matches(sample)]
    while any(len(codes) > 1 for codes in ops.values()):
        deduced_codes = [codes[0] for codes in ops.values() if len(codes) == 1]
        for num, codes in ops.items():
            if len(codes) > 1:
                ops[num] = [c for c in codes if c not in deduced_codes]
    return ops

def get_program_results(samples, program):
    """
        Get the result of the program
    """
    ops = get_opcode_mapping(samples)
    registers = [0, 0, 0, 0]
    for opcode, in1, in2, out in program:
        registers = ops[opcode][0](in1, in2, out, registers)
    return registers[0]


print(get_samples_matching_three_or_more(SAMPLES))
print(get_program_results(SAMPLES, PROGRAM))
