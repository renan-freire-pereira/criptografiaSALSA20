# Salsa20 Stream Cipher (eStream)

[cite_start]Este repositório contém uma implementação conceitual da cifra de fluxo **Salsa20**, uma alternativa moderna e eficiente pertencente ao projeto eStream, projetada para alta performance tanto em hardware quanto em software[cite: 106, 107].

---

##  Visão Geral do Funcionamento

[cite_start]A Salsa20 é uma cifra de fluxo simétrica que oculta a mensagem combinando seus bits/bytes continuamente com um fluxo de ruído pseudo-aleatório (keystream) gerado a partir de uma chave secreta e um nonce[cite: 87, 109]. 

[cite_start]O processo básico de criptografia e descriptografia baseia-se na operação XOR ($\oplus$)[cite: 109, 186]:

* [cite_start]**Criptografar:** $\text{Texto Cifrado} = \text{Mensagem} \oplus \text{Fluxo de Chave}$ [cite: 189]
* [cite_start]**Descriptografar:** $\text{Mensagem} = \text{Texto Cifrado} \oplus \text{Fluxo de Chave}$ [cite: 191]

[cite_start]O PseudoGerador de Valores Aleatórios (PRG) da Salsa20 expande a chave ($K$) de 128 ou 256 bits e um nonce ($r$) de 64 bits para gerar um fluxo de chave de até $2^{73}$ bits (1 trilhão de Gigabytes)[cite: 110, 112, 113, 117]:

[cite_start]$$PRG_{\text{Salsa20}}(k, r) = H(k, (r, 0)) \parallel H(k, (r, 1)) \parallel H(k, (r, 2)) \dots$$ [cite: 115]

---

##  Estrutura da Matriz (Função H)

[cite_start]Para gerar cada bloco de 64 bytes do fluxo de chave, a função $H$ organiza os dados de entrada (Chave Secreta, Constantes Mágicas, Nonce e Contador) em uma matriz $4 \times 4$ contendo 16 palavras de 4 bytes (32 bits cada)[cite: 120, 121]:

* [cite_start]**Chave Secreta ($K$):** Dividida em 8 partes ($K[0]$ a $K[7]$)[cite: 122].
* [cite_start]**Constantes Mágicas ($C$):** Divididas em 4 partes ($C[0]$ a $C[3]$)[cite: 123].
* [cite_start]**Nonce ($N$):** Dividido em 2 partes ($N[0]$ a $N[1]$)[cite: 123].
* [cite_start]**Contador:** Dividido em 2 partes ($\text{Contador}[0]$ a $\text{Contador}[1]$)[cite: 124].

[cite_start]A disposição interna da matriz segue o layout abaixo[cite: 125, 127]:

```python
matriz_salsa = [
    C[0], K[0], K[1], K[2],  # Linha 0
    K[3], C[1], N[0], N[1],  # Linha 1
    contador_valores[0], contador_valores[1], C[2], K[4],  # Linha 2
    K[5], K[6], K[7], C[3]   # Linha 3
]

http://googleusercontent.com/immersive_entry_chip/0
http://googleusercontent.com/immersive_entry_chip/1
http://googleusercontent.com/immersive_entry_chip/2
http://googleusercontent.com/immersive_entry_chip/3
