import veriloggen as vg
from instructions import mkInstrOutputs


def mkDec() -> vg.Module:
    m = vg.Module("decoer")
    clk = m.Input("clk", 1)
    rstn: vg.Input = m.Input("rstn", 1)
    enabled: vg.Input = m.Input("enabled", 1)
    pc: vg.Input = m.Input("pc", 32)
    instr_raw = m.Input("instr_raw", 32)

    instr = mkInstrOutputs(m, preffix="instr_")

    # classify instructions
    funct7: vg.Wire = m.Wire("funct7", 7)
    funct7.assign(instr_raw[25:32:1])
    funct3: vg.Wire = m.Wire("funct3", 3)
    funct3.assign(instr_raw[12:14:1])
    opcode: vg.Wire = m.Wire("opcode", 7)
    opcode.assign(instr_raw[:7:1])

    r_type: vg.Wire = m.Wire("r_type", 1)
    r_type.assign(vg.Or(opcode == 0b11110011, opcode == 0b1010011))
    i_type: vg.Wire = m.Wire("i_type", 1)
    i_type.assign(
        vg.Or(
            vg.Or(opcode == 0b1100111, opcode == 0b0000011),
            vg.Or(opcode == 0b0010011, opcode == 0b0000111),
        )
    )
    s_type: vg.Wire = m.Wire("s_type", 1)
    s_type.assign(vg.Or(opcode == 0b0100011, opcode == 0b0100111))
    b_type: vg.Wire = m.Wire("b_type", 1)
    b_type.assign(opcode == 0b1100011)
    u_type: vg.Wire = m.Wire("u_type", 1)
    u_type.assign(opcode == 0b0010111)
    j_type: vg.Wire = m.Wire("j_type", 1)
    j_type.assign(opcode == 0b1101111)

    instr["instr_lui"].assign(opcode == 0b0110111)
    instr["instr_auipc"].assign(opcode == 0b0010111)
    instr["instr_jal"].assign(opcode == 0b1101111)
    instr["instr_jalr"].assign(opcode == 0b1100111)
    #    conditional breaks
    instr["instr_beq"].assign(vg.And(opcode == 0b1100011, funct3 == 0b000))
    instr["instr_bne"].assign(vg.And(opcode == 0b1100011, funct3 == 0b001))
    instr["instr_ble"].assign(vg.And(opcode == 0b1100011, funct3 == 0b100))
    instr["instr_bge"].assign(vg.And(opcode == 0b1100011, funct3 == 0b101))
    instr["instr_bltu"].assign(vg.And(opcode == 0b1100011, funct3 == 0b110))
    instr["instr_bgeu"].assign(vg.And(opcode == 0b1100011, funct3 == 0b111))
    #    memory control
    instr["instr_lb"].assign(vg.And(opcode == 0b0000011, funct3 == 0b000))
    instr["instr_lh"].assign(vg.And(opcode == 0b0000011, funct3 == 0b001))
    instr["instr_lw"].assign(vg.And(opcode == 0b0000011, funct3 == 0b010))
    instr["instr_lbu"].assign(vg.And(opcode == 0b0000011, funct3 == 0b100))
    instr["instr_lhu"].assign(vg.And(opcode == 0b0000011, funct3 == 0b101))
    instr["instr_sb"].assign(vg.And(opcode == 0b0100011, funct3 == 0b000))
    instr["instr_sh"].assign(vg.And(opcode == 0b0100011, funct3 == 0b001))
    instr["instr_sw"].assign(vg.And(opcode == 0b0100011, funct3 == 0b010))
    #    arith immediate
    instr["instr_addi"].assign(vg.And(opcode == 0b0010011, funct3 == 0b000))
    instr["instr_slti"].assign(vg.And(opcode == 0b0010011, funct3 == 0b010))
    instr["instr_sltiu"].assign(vg.And(opcode == 0b0010011, funct3 == 0b011))
    instr["instr_xori"].assign(vg.And(opcode == 0b0010011, funct3 == 0b100))
    instr["instr_ori"].assign(vg.And(opcode == 0b0010011, funct3 == 0b110))
    instr["instr_andi"].assign(vg.And(opcode == 0b0010011, funct3 == 0b111))
    instr["instr_slli"].assign(vg.And(vg.And(opcode == 0b0010011, funct3 == 0b001), funct7 == 0b0000000))
    instr["instr_srli"].assign(vg.And(vg.And(opcode == 0b0010011, funct3 == 0b101), funct7 == 0b0000000))
    instr["instr_srai"].assign(vg.And(vg.And(opcode == 0b0010011, funct3 == 0b101), funct7 == 0b0100000))
    #    arith other
    instr["instr_add"].assign(vg.And(vg.And(opcode == 0b0110011, funct3 == 0b000), funct7 == 0b0000000))
    instr["instr_sub"].assign(vg.And(vg.And(opcode == 0b0110011, funct3 == 0b000), funct7 == 0b0100000))
    instr["instr_sll"].assign(vg.And(vg.And(opcode == 0b0110011, funct3 == 0b001), funct7 == 0b0000000))
    instr["instr_slt"].assign(vg.And(vg.And(opcode == 0b0110011, funct3 == 0b010), funct7 == 0b0000000))
    instr["instr_sltu"].assign(vg.And(vg.And(opcode == 0b0110011, funct3 == 0b011), funct7 == 0b0000000))
    instr["instr_srl"].assign(vg.And(vg.And(opcode == 0b0110011, funct3 == 0b101), funct7 == 0b0000000))
    instr["instr_sra"].assign(vg.And(vg.And(opcode == 0b0110011, funct3 == 0b111), funct7 == 0b0100000))


    # decode operands and immediates

    instr["instr_pc"].assign(pc)


    # _rs2: vg.Wire = m.Wire("rs2", 5)
    # _rs2.assign(instr_raw[20:25:1])
    instr["instr_rs2_addr"].assign(instr_raw[20:25:1])
    # _rs1: vg.Wire = m.Wire("rs1", 5)
    # _rs1.assign(instr_raw[15:20:1])
    instr["instr_rs1_addr"].assign(instr_raw[15:20:1])
    # _rd: vg.Wire = m.Wire("rd", 5)
    # _rd.assign(instr_raw[7:12:1])
    instr["instr_rd_addr"].assign(instr_raw[7:12:1])
    # FIXME: do synchronous
    # m.Always(vg.Posedge(clk))(
    #     vg.If(rstn)(
    #         vg.If(enabled)(
    #             # decode
    #             # instr["instr_rd_addr"].assign()
    #         )
    #     ).Else(
    #         # reset Inst
    #     )
    # )
    return m


if __name__ == "__main__":
    decoder = mkDec()
    verilog = decoder.to_verilog(filename="tmp.v")
    print(verilog)
