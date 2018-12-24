"""
    A list of opcodes
"""
from operator import add, mul, and_, or_, gt, eq
def apply_to_registers(registers, output, val1, val2, func):
    """
        Apply func(val1, val2) and saves it in registers[output]
    """
    registers[output] = func(val1, val2)
    return registers

def addi(register, value, output, registers):
    """
        Add immediate value to register
    """
    return apply_to_registers(registers, output, registers[register], value, add)

def addr(register1, register2, output, registers):
    """
        Add two registers together
    """
    return addi(register1, registers[register2], output, registers)

def muli(register, value, output, registers):
    """
        Multiply immediate value to register
    """
    return apply_to_registers(registers, output, registers[register], value, mul)

def mulr(register1, register2, output, registers):
    """
        Multiply two registers together
    """
    return muli(register1, registers[register2], output, registers)

def bani(register, value, output, registers):
    """
        Binary And register and immediate value
    """
    return apply_to_registers(registers, output, registers[register], value, and_)

def banr(register1, register2, output, registers):
    """
        Binary And two registers
    """
    return bani(register1, registers[register2], output, registers)

def bori(register, value, output, registers):
    """
        Binary Or register and immediate value
    """
    return apply_to_registers(registers, output, registers[register], value, or_)

def borr(register1, register2, output, registers):
    """
        Binary or two registers together
    """
    return bori(register1, registers[register2], output, registers)

def seti(value, _, output, registers):
    """
        Set an immediate value to a register
    """
    registers[output] = value
    return registers

def setr(register1, _, output, registers):
    """
        Set a register to another register value
    """
    return seti(registers[register1], _, output, registers)

def predicate(func):
    """
        Returns a function that will return 1 if true or 0 if false given two parameters
    """
    def inner(val1, val2):
        return 1 if func(val1, val2) else 0
    return inner

def gtir(value, register, output, registers):
    """
        Greater than Immediate > register
    """
    return apply_to_registers(registers, output, value, registers[register], predicate(gt))

def gtri(register, value, output, registers):
    """
        Greater than Register > immediate
    """
    return apply_to_registers(registers, output, registers[register], value, predicate(gt))

def gtrr(register1, register2, output, registers):
    """
        Greater than register > register
    """
    return gtri(register1, registers[register2], output, registers)

def eqir(value, register, output, registers):
    """
        Equal immediate to register
    """
    return apply_to_registers(registers, output, value, registers[register], predicate(eq))

def eqri(register, value, output, registers):
    """
        Equal register to immediate
    """
    return apply_to_registers(registers, output, value, registers[register], predicate(eq))

def eqrr(register1, register2, output, registers):
    """
        Equal register to register
    """
    return eqri(register1, registers[register2], output, registers)

OPCODES = [addi, addr, muli, mulr, bani, banr, bori,
           borr, seti, setr, gtri, gtir, gtrr, eqri, eqir, eqrr]

OPCODE_MAPPING = {
    "addi": addi,
    "addr": addr,
    "muli": muli,
    "mulr": mulr,
    "bani": bani,
    "banr": banr,
    "bori": bori,
    "borr": borr,
    "seti": seti,
    "setr": setr,
    "gtri": gtri,
    "gtir": gtir,
    "gtrr": gtrr,
    "eqri": eqri,
    "eqir": eqir,
    "eqrr": eqrr
}
