# x = int(input())
# y = int(input())

# maior = max(x, y)
# menor = min(x, y)

# soma = 0
# atual = menor + 1

# while atual < maior:
#     if atual % 2 != 0:
#         soma += atual
#     atual += 1

# print(soma)

# n = int(input())

# c = 1  

# fatorial = 1

# while c <= n:
#     fatorial *= c
#     c += 1

# print(fatorial)


# soma = 0

# c = True

# cont = 0

# while c:
#     n = int(input())
#     if n < 0:
#         c = False
#     soma += n
#     cont += 1
    
# media = soma/cont
# print(media)

n_casos = int(input())
caso_atual = 0

# Laço de fora: vai rodar exatamente "n_casos" vezes
while caso_atual < n_casos:
    x = int(input())
    
    soma_divisores = 0
    divisor = 1
    
    # Laço de dentro: procurar divisores
    # Vamos rodar do 1 até a metade de 'x' que já é suficiente
    while divisor <= x // 2:
        if x % divisor == 0:        # Verifica se o resto da divisão é 0 (ou seja, se é um divisor exato)
            soma_divisores += divisor
        
        divisor += 1               # Passamos para o próximo divisor para ir testando
        
    # Quando o laço de dentro acaba, a gente verifica se a soma deu o próprio número x
    if soma_divisores == x:
        print(f"{x} eh perfeito")
    else:
        print(f"{x} nao eh perfeito")
        
    # E então não podemos esquecer de contabilizar que lemos mais um caso!
    caso_atual += 1