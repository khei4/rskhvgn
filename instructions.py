from typing import Dict, Iterable
import veriloggen as vg

# ref: https://github.com/cpuex2019-7th/core/blob/master/src/def.sv
# name: width
# TODO: define instr class and use method to create as input and assign
decoded_instruction: Dict[str, int] = {
    # ports for data
    "rd_addr": 5,
    "rs1_addr": 5,
    "rs2_addr": 5,
    "imm": 32,
    "zimm": 32,
    "pc": 32,
    # "raw": 32,
    # ports for inst kind
    #    lui, auipc
    "lui": 1,
    "auipc": 1,
    #    jumps
    "jal": 1,
    "jalr": 1,
    #    conditional breaks
    "beq": 1,
    "bne": 1,
    "ble": 1,
    "bge": 1,
    "bltu": 1,
    "bgeu": 1,
    #    memory control
    "lb": 1,
    "lh": 1,
    "lw": 1,
    "lbu": 1,
    "lhu": 1,
    "sb": 1,
    "sh": 1,
    "sw": 1,
    #    arith immediate
    "addi": 1,
    "slti": 1,
    "sltiu": 1,
    "xori": 1,
    "ori": 1,
    "andi": 1,
    "slli": 1,
    "srli": 1,
    "srai": 1,
    #    arith other
    "add": 1,
    "sub": 1,
    "sll": 1,
    "slt": 1,
    "sltu": 1,
    "srl": 1,
    "sra": 1,
}

InstrInputs = Iterable[vg.Input]
InstrOutputs = Iterable[vg.Output]

def mkInstrInputs(m: vg.Module, preffix: str = "") -> InstrInputs:
    res = {}
    for name, value in decoded_instruction.items():
        n = preffix + name
        res[n] = m.Input(n, value)
    return res

def mkInstrOutputs(m: vg.Module, preffix: str = "") -> InstrOutputs:
    res = {}
    for name, value in decoded_instruction.items():
        n = preffix + name
        res[n] = m.Output(n, value)
    return res

def resetInstrInputs(instrs: InstrInputs):
    for i in instrs:
        i.assign(0)

def resetInstrInputs(instrs: InstrOutputs):
    for i in instrs:
        i.assign(0)