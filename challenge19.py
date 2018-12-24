"""
    Advent of Code 2019 Challenge 19
"""
from common.input_file import read_strings
from common.opcodes import OPCODE_MAPPING

def to_opcode(op_str: str):
    """
        Convert to an opcode
    """
    opcode, reg1, reg2, output = op_str.split()
    return OPCODE_MAPPING[opcode], int(reg1), int(reg2), int(output)


def get_program_value(instructions, instruction_register, registers):
    """
        Get the program value in register 0
    """
    instruction_pointer = 0
    while 0 <= instruction_pointer < len(instructions):
        registers[instruction_register] = instruction_pointer
        instruction, reg1, reg2, output = instructions[instruction_pointer]
        registers = instruction(reg1, reg2, output, registers)
        instruction_pointer = registers[instruction_register] + 1
    return registers[0]

def get_actual_value(target) -> int:
    """
        the assembly given is actually just a sum all divisors of a number
    """
    return sum(x for x in range(1, target+1) if target % x == 0)

FILE_TEXT = read_strings("input/input19.txt")
INSTRUCTION_REGISTER = int(FILE_TEXT[0].split()[-1])
INSTRUCTIONS = list(map(to_opcode, FILE_TEXT[1:]))

if __name__ == "__main__":
    print(get_actual_value(875))
    print(get_actual_value(10551275))
