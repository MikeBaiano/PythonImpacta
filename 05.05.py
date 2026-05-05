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

    