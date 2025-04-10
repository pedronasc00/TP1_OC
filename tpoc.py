linha = input("Digite a instrução: ")
# Remove vírgulas e divide a linha em pedaços
linha = linha.replace(',', '')
partes = linha.strip().split()
# Trata de acordo com a quantidade de pedaços
if len(partes) == 4:
    instr, op1, op2, op3 = partes
elif len(partes) == 3:
    instr, op1, op2 = partes
    