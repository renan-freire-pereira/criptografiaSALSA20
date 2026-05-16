import os

def salsa20_256bytes(M, K, r, modo="criptografar"):
    fluxo = ""
    retorno = ""
    

    if modo == "criptografar":
        tmp = M
        M = ""
        for m in tmp:
            M += f"{ord(m):08b}"
    else:
        M = M.strip()

    def rotl32(x, n):
        return ((x << n) & 0xffffffff) | (x >> (32 - n))

    def quarter_round(x, a, b, c, d):
        x[b] ^= rotl32((x[a] + x[d]) & 0xffffffff, 7)
        x[c] ^= rotl32((x[b] + x[a]) & 0xffffffff, 9)
        x[d] ^= rotl32((x[c] + x[b]) & 0xffffffff, 13)
        x[a] ^= rotl32((x[d] + x[c]) & 0xffffffff, 18)

    contador = 0

    while len(fluxo) < len(M): 
        C = [0x61707865, 0x3120646e, 0x79622d36, 0x6b206574]

        C0 = contador & 0xffffffff 
        C1 = (contador >> 32) & 0xffffffff 

        K0 = K & 0xffffffff
        K1 = (K >> 32)  & 0xffffffff
        K2 = (K >> 64)  & 0xffffffff
        K3 = (K >> 96)  & 0xffffffff
        K4 = (K >> 128) & 0xffffffff
        K5 = (K >> 160) & 0xffffffff
        K6 = (K >> 192) & 0xffffffff
        K7 = (K >> 224) & 0xffffffff

        N0 = r & 0xffffffff
        N1 = (r >> 32) & 0xffffffff

        matriz_salsa = [
            C[0], K0,  K1,  K2,  
            K3,   C[1],N0,  N1,  
            C0,   C1,  C[2],K4,  
            K5,   K6,  K7,  C[3]   
        ]

        matriz_salsa_original = list(matriz_salsa)

        for _ in range(10):
            quarter_round(matriz_salsa, 0, 4, 8, 12)
            quarter_round(matriz_salsa, 5, 9, 13, 1)
            quarter_round(matriz_salsa, 10, 14, 2, 6)
            quarter_round(matriz_salsa, 15, 3, 7, 11)
            
            quarter_round(matriz_salsa, 0, 1, 2, 3)
            quarter_round(matriz_salsa, 5, 6, 7, 4)
            quarter_round(matriz_salsa, 10, 11, 8, 9)
            quarter_round(matriz_salsa, 15, 12, 13, 14)

        bloco_soma = []
        for i in range(16):
            resultado = (matriz_salsa[i] + matriz_salsa_original[i]) & 0xffffffff
            bloco_soma.append(resultado)

        for valor in bloco_soma:
            fluxo += f"{valor:032b}"

        contador += 1

    for i in range(len(M)):
        bit_xor = int(fluxo[i]) ^ int(M[i])
        retorno += str(bit_xor)

    return retorno

print("=============================================")
print(" == CRIPTOGRAFIA/DESCRIPTOGRAFIA DE ARQUIVOS COM SALSA20 ==")

acao = int(input("Deseja criptografar (0) ou descriptografar? (1): "))

if acao == 0:
    print(" == MODO CRIPTOGRAFIA ==\n")

    nome = input("Qual o nome do arquivo de texto (omitir .txt)? ")
    with open(nome + ".txt", "r", encoding="UTF-8") as arquivo:
        mensagem = arquivo.read()

    k_bytes = os.urandom(32)
    r_bytes = os.urandom(8)

    K = int.from_bytes(k_bytes, "little")
    r = int.from_bytes(r_bytes, "little")

    texto_criptografado = salsa20_256bytes(mensagem, K, r, modo="criptografar")

    with open(nome + ".txt", "w", encoding="UTF-8") as arquivoCriptografado:
        arquivoCriptografado.write(texto_criptografado)

    with open(nome + "_semente.txt", "w", encoding="UTF-8") as arquivoSemente:
        arquivoSemente.write(k_bytes.hex())

    with open(nome + "_nonce.txt", "w", encoding="UTF-8") as arquivoNonce:
        arquivoNonce.write(r_bytes.hex())

    print("\n== ARQUIVOS GERADOS COM SUCESSO ==")

else:
    print(" == MODO DESCRIPTOGRAFIA ==\n")

    endSemente = input("Digite o nome do arquivo com a semente (omitir .txt): ") + ".txt"
    endNonce = input("Digite o nome do arquivo com o nonce (R) (omitir .txt): ") + ".txt"
    endMensagem = input("Digite o nome do arquivo com a mensagem criptografada (omitir .txt): ") + ".txt"

    with open(endSemente, "r", encoding="UTF-8") as f:
        k_bytes = bytes.fromhex(f.read().strip())
        K = int.from_bytes(k_bytes, "little")
        
    with open(endNonce, "r", encoding="UTF-8") as f:
        r_bytes = bytes.fromhex(f.read().strip())
        r = int.from_bytes(r_bytes, "little")
        
    with open(endMensagem, "r", encoding="UTF-8") as f:
        mensagem_criptografada = f.read()

    bits_descriptografados = salsa20_256bytes(mensagem_criptografada, K, r, modo="descriptografar")

    mensagem_original = ""
    for i in range(0, len(bits_descriptografados), 8):
        byte = bits_descriptografados[i:i+8]
        if len(byte) == 8:
            mensagem_original += chr(int(byte, 2))

    nome_saida = endMensagem.replace("_criptografado.txt", "").replace(".txt", "")
    with open(nome_saida + ".txt", "w", encoding="UTF-8") as arquivoDescriptografado:
        arquivoDescriptografado.write(mensagem_original)

    print(f"\n Mensagem descriptografada com sucesso!")
    print(f"Arquivo gerado: {nome_saida}.txt")
    print(f"Conteúdo: {mensagem_original}")
