from assembler import *

def main():
    args = sys.argv
    if len(args) == 4 and args[2] == "-o":
        arq_entrada = args[1]
        arq_saida = args[3]
        saidas_binarias = []
        try:
            with open(arq_entrada, 'r') as arquivo:
                linhas = arquivo.readlines()
                for linha in linhas:
                    instr, rd, rs1, rs2, imediato = ler_instrucao(linha)
                    if instr is not None:
                        binario = montar_instrucao(instr, rd, rs1, rs2, imediato)
                        if binario:
                            saidas_binarias.append(binario)
            with open(arq_saida, "w") as saida:
                for linha in saidas_binarias:
                    saida.write(linha + "\n")
            print(f"Instruções convertidas salvas em '{arq_saida}'")
        except FileNotFoundError:
            print("Arquivo de entrada não encontrado.")

    elif len(args) < 2:
        linhas = []
        print("Digite instruções linha por linha. Para encerrar digite 'fim'.\n")
        while True:
            linha = input("> ")
            if linha.lower() == 'fim':
                break
            linhas.append(linha)

        for linha in linhas:
            instr, rd, rs1, rs2, imediato = ler_instrucao(linha)
            if instr is not None:
                binario = montar_instrucao(instr, rd, rs1, rs2, imediato)
                if binario:
                    print(binario)              

if __name__ == "__main__" :

    main();