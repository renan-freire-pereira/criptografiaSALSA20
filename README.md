Salsa20 Stream Cipher (eStream)

Este repositório contém uma implementação conceitual da cifra de fluxo Salsa20, uma alternativa moderna e eficiente pertencente ao projeto eStream, projetada para alta performance tanto em hardware quanto em software.

Visão Geral do Funcionamento

A Salsa20 é uma cifra de fluxo simétrica que oculta a mensagem combinando seus bits ou bytes continuamente com um fluxo de ruído pseudo-aleatório (keystream) gerado a partir de uma chave secreta e um nonce.

O processo básico de criptografia e descriptografia baseia-se na operação XOR ($\oplus$):

Criptografar: $\text{Texto Cifrado} = \text{Mensagem} \oplus \text{Fluxo de Chave}$

Descriptografar: $\text{Mensagem} = \text{Texto Cifrado} \oplus \text{Fluxo de Chave}$

O PseudoGerador de Valores Aleatórios (PRG) da Salsa20 expande a chave ($K$) de 128 ou 256 bits e um nonce ($r$) de 64 bits para gerar um fluxo de chave de até $2^{73}$ bits (aproximadamente 1 trilhão de Gigabytes):

$$PRG_{\text{Salsa20}}(k, r) = H(k, (r, 0)) \parallel H(k, (r, 1)) \parallel H(k, (r, 2)) \dots$$

Estrutura da Matriz (Função H)

Para gerar cada bloco de 64 bytes do fluxo de chave, a função $H$ organiza os dados de entrada (Chave Secreta, Constantes Mágicas, Nonce e Contador) em uma matriz $4 \times 4$ contendo 16 palavras de 4 bytes (32 bits cada):

Chave Secreta ($K$): Dividida em 8 partes ($K[0]$ a $K[7]$).

Constantes Mágicas ($C$): Divididas em 4 partes ($C[0]$ a $C[3]$).

Nonce ($N$): Dividido em 2 partes ($N[0]$ a $N[1]$).

Contador: Dividido em 2 partes ($\text{Contador}[0]$ a $\text{Contador}[1]$).

A disposição interna da matriz segue o layout abaixo:

matriz_salsa = [
    C[0], K[0], K[1], K[2],  # Linha 0
    K[3], C[1], N[0], N[1],  # Linha 1
    contador_valores[0], contador_valores[1], C[2], K[4],  # Linha 2
    K[5], K[6], K[7], C[3]   # Linha 3
]


Core do Algoritmo

O processamento da matriz consiste na função quarter_round e nas operações de rotação de bits.

1. Rotação de Bits (rotl32)

Função para rotacionar os bits de um inteiro de 32 bits para a esquerda por $n$ posições:

def rotl32(x, n):
    return ((x << n) & 0xffffffff) | (x >> (32 - n))


2. Função quarter_round

Modifica os valores diretamente na matriz utilizando adições modulares, XOR e rotações:

def quarter_round(x, a, b, c, d):
    x[b] ^= rotl32((x[a] + x[d]) & 0xffffffff, 7)
    x[c] ^= rotl32((x[b] + x[a]) & 0xffffffff, 9)
    x[d] ^= rotl32((x[c] + x[b]) & 0xffffffff, 13)
    x[a] ^= rotl32((x[d] + x[c]) & 0xffffffff, 18)


Rodadas de Embaralhamento

O algoritmo executa 10 iterações. Cada iteração contém uma rodada para colunas e uma rodada para linhas, totalizando as 20 rodadas:

for i in range(10):
    # Rodadas Ímpares: Colunas
    quarter_round(matriz_salsa, 0, 4, 8, 12)
    quarter_round(matriz_salsa, 5, 9, 13, 1)
    quarter_round(matriz_salsa, 10, 14, 2, 6)
    quarter_round(matriz_salsa, 15, 3, 7, 11)
    
    # Rodadas Pares: Linhas
    quarter_round(matriz_salsa, 0, 1, 2, 3)
    quarter_round(matriz_salsa, 5, 6, 7, 4)
    quarter_round(matriz_salsa, 10, 11, 8, 9)
    quarter_round(matriz_salsa, 15, 12, 13, 14)


Após o processamento, a matriz resultante é somada à matriz original para gerar os 64 bytes do fluxo de chave.
