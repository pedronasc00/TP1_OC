# import re

# instrucoes = {
#     "lb": {"Format": "I", "Opcode": '0000011', "funct3": '000', "funct7": '0000000'},
#     "sb": {"Format": "S", "Opcode": '0100011', "funct3": '000', "funct7": "0000000"},
#     "sub": {"Format": "R", "Opcode": "0110011", "funct3": "000", "funct7": "0100000"},
#     "and": {"Format": "R","Opcode": '0110011', "funct3": '111', "funct7": "0000000"},
#     "ori": {"Format": "I", "Opcode": '0010011', "funct3": '110', "funct7": "0000000"},
#     "slr": {"Format": "R", "Opcode": '0010011', "funct3": '101', "funct7": "0000000"},
#     "beq": {"Format": "SB", "Opcode": '1100111', "funct3": '000', "funct7": "0000000"}
# }

# def ler_instrucao(linha):
#     instrucao = linha.strip().replace(",", "")
#     parte = instrucao.split()

#     if len(parte) == 4:
#         instr = parte[0]
#         rd = parte[1]
#         rs1 = parte[2]
#         rs2 = parte[3]
#     elif len(parte) == 3:
#         instr = parte[0]
#         rd = parte[1]
#         rs1 = parte[2]
#         rs2 = None
#     else:
#         print("erro na linha escrita")
#         return None
    
#     return instr, rd, rs1, rs2

# def conversao_binaria(rd, rs1, rs2):
#     # Função auxiliar para converter o número após o 'x' em binário
#     def converter_para_binario(valor):
#         # Se o valor contiver 'x', converte o número após o 'x'
#         if 'x' in valor:
#             # Se o valor contiver parênteses, pega o número dentro dos parênteses
#             if '(' in valor and ')' in valor:
#                 numero = int(re.findall(r'\d+', valor.split('x')[1])[0])  # Pega o número após 'x' e dentro dos parênteses
#             else:
#                 numero = int(re.findall(r'\d+', valor)[0])  # Caso normal, apenas número após o 'x'
#             return format(numero, '05b')  # Converte para binário com 5 bits
#         return None  # Caso não tenha 'x', retorna None

#     # Converte os valores de rd, rs1 e rs2, se houver um número após 'x'
#     rd_bin = converter_para_binario(rd)
#     rs1_bin = converter_para_binario(rs1)
    
#     # Converte rs2 apenas se não for None
#     rs2_bin = converter_para_binario(rs2) if rs2 is not None else None

#     # Retorna os resultados
#     return rd_bin, rs1_bin, rs2_bin
        
# if __name__ == "__main__" :

#     opcao = input("Escolha 1(ler pelo arquivo) ou 2(executar pelo terminal): ")
#     if opcao == "1":
#         n_arquivo = input("Digite o nome do arquivo .asm: ")
#         resultado = ler_arquivo(n_arquivo)
#     elif opcao == "2":
#         resultado = input()
#         isntr, rd, rs1, rs2 = ler_instrucao(resultado)
#         rd_bin, rs1_bin, rs2_bin = conversao_binaria(rd, rs1, rs2)
#         print(f"rd: {rd_bin}, rs1: {rs1_bin}, rs2_bin: {rs2_bin}")

#     else:
#         print("Opção inválida.")

import re

instrucoes = {
    "lb":  {"Format": "I",  "Opcode": '0000011', "funct3": '000', "funct7": '0000000'},
    "sb":  {"Format": "S",  "Opcode": '0100011', "funct3": '000', "funct7": '0000000'},
    "sub": {"Format": "R",  "Opcode": '0110011', "funct3": '000', "funct7": '0100000'},
    "and": {"Format": "R",  "Opcode": '0110011', "funct3": '111', "funct7": '0000000'},
    "ori": {"Format": "I",  "Opcode": '0010011', "funct3": '110', "funct7": '0000000'},
    "slr": {"Format": "R",  "Opcode": '0010011', "funct3": '101', "funct7": '0000000'},
    "beq": {"Format": "SB", "Opcode": '1100111', "funct3": '000', "funct7": '0000000'}
}

def ler_instrucao(linha):
    linha = linha.strip().replace(",", "")
    partes = linha.split()

    instr = partes[0]
    rs = partes[1:]

    return instr, rs

def extrair_registro(valor):
    if 'x' in valor:
        return format(int(re.findall(r'\d+', valor)[0]), '05b')
    return None

def extrair_imediato(valor):
    if '(' in valor:
        imm = int(valor.split('(')[0])
        return format(imm & 0xFFF, '012b')  # Para I-type
    else:
        return format(int(valor), '012b')

def montar_instrucao(instr, rs):
    if instr not in instrucoes:
        print("Instrução inválida.")
        return
    
    info = instrucoes[instr]
    fmt = info["Format"]
    opcode = info["Opcode"]
    funct3 = info["funct3"]
    funct7 = info["funct7"]

    if fmt == "R":
        rd  = extrair_registro(rs[0])
        rs1 = extrair_registro(rs[1])
        rs2 = extrair_registro(rs[2])
        print(f"{funct7} {rs2} {rs1} {funct3} {rd} {opcode}")

    elif fmt == "I":
        rd  = extrair_registro(rs[0])
        if '(' in rs[1]:
            imm = format(int(rs[1].split('(')[0]), '012b')
            rs1 = extrair_registro(rs[1])
        else:
            rs1 = extrair_registro(rs[1])
            imm = format(int(rs[2]), '012b')
        print(f"{imm} {rs1} {funct3} {rd} {opcode}")

    elif fmt == "S":
        rs2 = extrair_registro(rs[0])
        rs1 = extrair_registro(rs[1])
        imm_total = int(rs[1].split('(')[0])
        imm = format(imm_total & 0xFFF, '012b')
        imm_11_5 = imm[:7]
        imm_4_0 = imm[7:]
        print(f"{imm_11_5} {rs2} {rs1} {funct3} {imm_4_0} {opcode}")

    elif fmt == "SB":
        rd  = extrair_registro(rs[0])
        rs1 = extrair_registro(rs[1])
        rs2 = extrair_registro(rs[2])
        imm = format(4, '012b')  # Apenas um exemplo de imediato de 12 bits
        imm_11_5 = imm[:7]
        print(f"{imm_11_5} {rs2} {rs1} {funct3} {rd} {opcode}")

if __name__ == "__main__":
    linha = input("Digite a instrução: ")
    instr, rs = ler_instrucao(linha)
    montar_instrucao(instr, rs)