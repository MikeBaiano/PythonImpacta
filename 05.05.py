# def soma_matriz(matriz_dados):
#     soma = 0
#     for i in range(len(matriz_dados)):
#         for j in range(len(matriz_dados[i])):
#             soma += matriz_dados[i][j]
#     return soma

# matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# print("A soma dos elementos da matriz é:", soma_matriz(matriz))
    
def inverte_matriz(matriz_dados):
    for i in range(len(matriz_dados)):
        for j in range(len(matriz_dados[i])):
            matriz_dados[i][j] *= -1
    return matriz_dados


matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print("A matriz invertida é:", inverte_matriz(matriz))
print(matriz)

# Beecrowd 1172 - Substituição em Vetor

x = []

for i in range(10):
    j = int(input())
    x.append(j)
    
for i in range(len(x)):
    if x[i] <= 0:
        x[i] = 1

    print(f"X[{i}] = {x[i]}")

# Beecrowd 1173 - Preenchimento de Vetor

x = int(input())

n = [x]

for i in range(9):
    x *= 2
    n.append(x)
    
for i in range(len(n)):
    print(f'N[{i}] = {n[i]}')

# Beecrowd 1174 - Seleção em Vetor

n = []

for i in range(100):
    x = float(input())
    n.append(x)
    
for i in range(len(n)):
    if n[i] <= 10:
        print(f'A[{i}] = {n[i]}')

# Beecrowd 1175 - Troca em Vetor

n = []

for i in range(20):
    n.append(int(input()))
for i in range(10):
    n[i], n[19-i] = n[19-i], n[i]
    
for i in range(20):
    print(f"N[{i}] = {n[i]}")

# Beecrowd 1177 - Preenchimento de Vetor

t = int(input())

n = []

c = 0
x = 0

for i in range(1000):
    if x >= t:
        x = 0
    print(f'N[{i}] = {x}')
    x += 1