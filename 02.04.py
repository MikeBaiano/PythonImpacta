# N = int(input())

# a = 1

# while a <= N:
#     if a % 2 == 0:
#         print(f"{a}^2 = {a**2}")
#     a += 1

posicao = 0
maior = 0
a = 1

while a <= 100:
    n = int(input())
    
    if n > maior:
        maior = n
        posicao = a # Sem acento para não dar erro
        
    a += 1

print(maior)
print(posicao)