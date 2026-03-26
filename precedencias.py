# Demonstrando a precedência de operadores matemáticos em Python
# A precedência (ordem de execução) da maior para a menor é:
# 1. Parênteses ()
# 2. Exponenciação **
# 3. Multiplicação *, Divisão /, Divisão Inteira //, Módulo % (avaliados da esquerda para a direita)
# 4. Adição +, Subtração - (avaliados da esquerda para a direita)

print("--- Demonstração de Precedência de Operadores ---")

print("\n1. Exponenciação (**) vs Multiplicação/Divisão (//):")
# Exemplo 1: 2 * 3 ** 2
# Como ** tem precedência maior, calcula-se primeiro 3 ** 2 = 9, depois 2 * 9 = 18
resultado1 = 2 * 3 ** 2
print(f"2 * 3 ** 2 = {resultado1}")

# Exemplo 2: 10 // 2 ** 2
# Primeiro 2 ** 2 = 4, depois 10 // 4 = 2 (divisão inteira de 10 por 4)
resultado2 = 10 // 2 ** 2
print(f"10 // 2 ** 2 = {resultado2}")

print("\n2. Divisão Inteira (//) vs Adição/Subtração (+, -):")
# Exemplo 3: 10 + 15 // 4
# Como // tem precedência maior, calcula-se 15 // 4 = 3, depois 10 + 3 = 13
resultado3 = 10 + 15 // 4
print(f"10 + 15 // 4 = {resultado3}")

print("\n3. Exponenciação (**) vs Uso de Parênteses ():")
# Exemplo 4: (2 * 3) ** 2
# Parênteses têm a maior precedência, então 2 * 3 = 6, depois 6 ** 2 = 36
resultado4 = (2 * 3) ** 2
print(f"(2 * 3) ** 2 = {resultado4}")

print("\n4. Avaliação da esquerda para a direita (mesma precedência):")
# Exemplo 5: 20 // 3 * 2
# // e * têm a mesma precedência, então avalia-se da esquerda para a direita: 20 // 3 = 6, depois 6 * 2 = 12
resultado5 = 20 // 3 * 2
print(f"20 // 3 * 2 = {resultado5}")

print("\n5. Juntando tudo (**, //, +, -):")
# Exemplo 6: 50 - 2 ** 3 * 4 // 3 + 5
# 1. Exponenciação: 2 ** 3 = 8
# 2. Multiplicação/Divisão da esq p/ dir: 8 * 4 = 32 -> 32 // 3 = 10
# 3. Adição/Subtração da esq p/ dir: 50 - 10 = 40 -> 40 + 5 = 45
resultado6 = 50 - 2 ** 3 * 4 // 3 + 5
print(f"50 - 2 ** 3 * 4 // 3 + 5 = {resultado6}")
