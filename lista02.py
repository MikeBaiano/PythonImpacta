# Questão 1: Cálculo de Área de Trapézio
# # Algoritmo que calcula a área de um trapézio usando a fórmula A = (B + b) * h / 2

# print("=== Cálculo da Área de um Trapézio ===")
# print()

# # Entrada de dados - leitura das variáveis
# B = float(input("Digite a base maior (B): "))
# b = float(input("Digite a base menor (b): "))
# h = float(input("Digite a altura (h): "))

# # Processamento - cálculo da área
# A = (B + b) * h / 2

# # Saída - exibição do resultado
# print()
# print(f"A área do trapézio é: {A}")

# # Questão 2: Verificação de maioridade
# # Algoritmo que verifica se uma pessoa é maior de idade (18 anos)

# print("=== Verificação de Maioridade ===")
# print()

# # Entrada de dados - leitura da variável
# idade = int(input("Digite a idade da pessoa: "))

# # Processamento - verificação da maioridade
# if idade >= 18:
#     print()
#     print("✓ A pessoa é maior de idade!")
# else:
#     print()
#     print("✗ A pessoa é menor de idade!")

# Questão 3: Cálculo de desconto em compras
# Algoritmo que calcula o desconto em uma compra. Se o valor da compra for acima de 200 reais, se aplica um desconto de 15%. Caso contrário, não se aplica desconto.

# print("=== Cálculo de Desconto em Compras ===")
# print()

# # Entrada de dados - leitura das variáveis
# valor_compra = float(input("Digite o valor da compra: "))

# if valor_compra > 200:
#     desconto = valor_compra * 0.15
# else:
#     desconto = 0

# valor_final = valor_compra - desconto

# print()
# print(f"O valor final da compra é: {valor_final}")

# Questão 4: Cálculo de média de 5 números
# Algoritmo que calcula a média de 5 números usando while loop

soma = 0
cont = 0

while cont < 5:
    num = float(input("Digite um número: "))
    soma += num
    cont += 1

media = soma / cont
print()
print(f"A média dos 5 números é: {media}")

# Questão 5: Escrever a tabuada de um numero de 1 a 10
# Algoritmo que escreve a tabuada de um numero de 1 a 10

numero = int(input("Digite um número: "))

for i in range(1, 11):
    print(f"{numero} x {i} = {numero * i}")
