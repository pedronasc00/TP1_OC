import re

instrucoes = {
    "add": {"Format": "R", "Opcode": "0110011", "funct3": "000", "funct7": "0000000"},
    "sub": {"Format": "R", "Opcode": "0110011", "funct3": "000", "funct7": "0100000"},
    "add": {"Format": "R", "Opcode": "0110011", "funct3": "000", "funct7": "0000000"},
    "and": {"Format": "R","Opcode": '0110011', "funct3": '111', "funct7": "0000000"},
    "or":  {"Format": "R","Opcode": '0110011', "funct3": '110', "funct7": "0000000"},
    "xor": {"Format": "R","Opcode": '0110011', "funct3": '100', "funct7": "0000000"},
    "slr": {"Format": "R", "Opcode": '0110011', "funct3": '101', "funct7": "0000000"},
    "sll": {"Format": "R", "Opcode": '0110011', "funct3": '001', "funct7": "0000000"},
    
    "sb": {"Format": "S", "Opcode": '0100011', "funct3": '000', "funct7": None},
    "sh": {"Format": "S", "Opcode": '0100011', "funct3": '001', "funct7": None},
    "sw": {"Format": "S", "Opcode": '0100011', "funct3": '010', "funct7": None},
    
    "beq": {"Format": "SB", "Opcode": '1100111', "funct3": '000', "funct7": None},
    "bne": {"Format": "SB", "Opcode": '1100111', "funct3": '001', "funct7": None},
    
    "lb": {"Format": "I", "Opcode": '0000011', "funct3": '000', "funct7": None},
    "lh": {"Format": "I", "Opcode": '0000011', "funct3": '001', "funct7": None},
    "lw": {"Format": "I", "Opcode": '0000011', "funct3": '010', "funct7": None},
    "addi": {"Format": "I", "Opcode": '0010011', "funct3": '000', "funct7": None},
    "ori": {"Format": "I", "Opcode": '0010011', "funct3": '110', "funct7": None},
    "andi": {"Format": "I", "Opcode": '0010011', "funct3": '111', "funct7": None},
}

def ler_instrucao(linha):
    instrucao = linha.strip().replace(",", "")
    parte = instrucao.split()

    instr = None   
    rd = None
    rs1 = None
    rs2 = None
    imm = None
    
    if len(parte) == 4:
        instr = parte[0]
        rd = parte[1]
        rs1 = parte[2]
        if parte[3].startswith("x"):
            rs2 = parte[3]
        else:
            imm = parte[3]

    elif len(parte) == 3:
        instr = parte[0]
        rd = parte[1]
        if '(' in parte[2]:
            match = re.match(r"(-?\d+)\(x(\d+)\)", parte[2])
            if match:
                imm = match.group(1)
                rs1 = "x" + match.group(2)
        else:
            rs1 = parte[2]
    
    else:
        print("erro na linha escrita")
        return None, None, None, None, None
    
    return instr, rd, rs1, rs2, imm

def conversao_binaria(valor):
    if valor is None:
        return None
        
    if valor.startswith("x"):
        num_str = valor.split('x')[1]
        numero = int(num_str)
        return format(numero, '05b')

    elif valor.startswith("0b"):
        v_binario =  valor[2:]
        return v_binario.zfill(5) if len(v_binario) < 5 else v_binario

    elif valor.startswith("0x") or valor.startswith("-0x"):
        numero = int(valor, 16)
        return format(numero & 0x1F, '05b')
    
    elif (valor.isdigit()) or (valor.startswith('-') and valor[1:].isdigit()):
        numero = int(valor)
        return format(numero, '05b')

    return None

def extrair_imediato(imm, Format):
    if imm is None:
        return

    if imm.startswith("0x"):
        imm = int(imm, 16)
    elif imm.startswith("-0x"):
        imm = -int(imm[3:], 16)
    elif '-' in imm:
        imm = int(imm) * -1
    else:
        imm = int(imm)
    
    if Format == 'I':
        return format(imm & 0xFFF, '012b')
    elif Format == 'S':
        return format(imm & 0xFFF, '012b')
    elif Format == 'SB':
        return format(imm & 0xFFF, '013b')
    

def montar_instrucao(instr, rd, rs1, rs2, imm):
    if instr not in instrucoes:
        print("Instrução inválida")
        return None
    
    info = instrucoes[instr]
    fmt = info["Format"]
    opcode = info["Opcode"]
    funct3 = info["funct3"]
    funct7 = info.get("funct7", "")
    
    rd_bin = conversao_binaria(rd)
    rs1_bin = conversao_binaria(rs1) if fmt != "U" else extrair_imediato(rs1, fmt)
    rs2_bin = conversao_binaria(rs2)  
    imm_bin = extrair_imediato(imm, fmt)

    if fmt == "R":
        rs2_bin = imm_bin if rs2_bin is None else rs2_bin
        return f"{funct7}{rs2_bin}{rs1_bin}{funct3}{rd_bin}{opcode}"
        # funct7: 7 bits | rs2: 5 bits | rs1: 5 bits | funct3: 3 bits | rd: 5 bits | opcode: 7 bits
    elif fmt == "I":
        return f"{imm_bin}{rs1_bin}{funct3}{rd_bin}{opcode}"
        # imm[11:0]: 12 bits | rs1: 5 bits | funct3: 3 bits | rd: 5 bits | opcode: 7 bits
    elif fmt == "S":
        rs2_bin = imm_bin if rs2_bin is None else rs2_bin
        imm_inter = imm_bin[:7] if imm_bin is not None else "0000000"
        imm_ext = imm_bin[7:] if imm_bin is not None else "00000"
        
        return f"{imm_inter}{rs2_bin}{rs1_bin}{funct3}{imm_ext}{opcode}"
        # imm[11:5]: 7 bits | rs2: 5 bits | rs1: 5 bits | funct3: 3 bits | imm[4:0]: 5 bits | opcode: 7 bits
    elif fmt == "SB":
        rs2_bin = imm_bin if rs2_bin is None else rs2_bin
        imm_inter = imm_bin[0] + imm_bin[2:8] if imm_bin  is not None else "0000000"
        imm_ext = imm_bin[8:12] + imm_bin[1] if imm_bin is not None else "00000"
        
        return f"{imm_inter}{rs2_bin}{rs1_bin}{funct3}{imm_ext}{opcode}"
        # imm[11:5]: 7 bits | rs2: 5 bits | rs1: 5: bits | funct3: 3 bits | rd: 5 bits | opcode: 7 bits
    return None
