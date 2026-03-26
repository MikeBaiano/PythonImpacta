import math as mt

# num_semana = int(input("Digite o número da semana: "))

# if num_semana == 1:
#     print("Domingo")
# elif num_semana == 2:
#     print("Segunda-feira")
# elif num_semana == 3:
#     print("Terça-feira")
# elif num_semana == 4:
#     print("Quarta-feira")
# elif num_semana == 5:
#     print("Quinta-feira")
# elif num_semana == 6:
#     print("Sexta-feira")
# elif num_semana == 7:
#     print("Sábado")
# else:
#     print("Número inválido!")

# nome = "Paula"
# idade = 25

# print("Olá, " + nome + "! Você tem " + str(idade) + " anos.")

# def soma(n1, n2):
#     s = n1 + n2
#     return s

# print(soma(10, 20))

# def par_impar(n):
#     if n % 2 == 0:
#         return "Sim"
#     else:
#         return "Não"



# print(f'{10} é par? {par_impar(10)}')
# print(f'{11} é par? {par_impar(11)}')

# print(f'O valor de pi é {mt.pi:.200f}')

# X = int(input())
# # range vai de 1 até X (colocamos X + 1 e a função para antes dele)
# for i in range(1, X + 1):
#     if i % 2 != 0: # Checa se o resto da divisão por 2 é diferente de zero
#         print(i)

# x = int(input())
# y = int(input())

# menor = min(x, y)
# maior = max(x, y)

# soma = 0

# for i in range(menor + 1, maior):
#     if i % 2 != 0:
#         soma += i
        
# print(soma)

# n = int(input())

# for i in range(1, n + 1):
#     if i % 2 == 0:
#         print(f'{i}^{2} = {i**2}')

maior = 0
posição = 0

for i in range(1, 101):
    n = int(input())
    if n > maior:
        maior = n
        posição = i

print(maior)
print(posição)

numero = 5
fatorial = 1  # Começamos em 1 porque ele é o elemento neutro da multiplicação
# Fazemos o loop girar do 1 até o número desejado
for i in range(1, numero + 1):
    fatorial = fatorial * i
print(fatorial)  # Vai imprimir 120

x = int(input())

for i in range(1, x + 1):
    if i % 2 !=0:
        print(i)

# Contagem de itens com crédito

credito = float(input('Seu crédito: '))
total = 0
contador = 1

preco = float(input('Preço do item: '))
while credito >= preco:
    total += preco
    credito -= preco
    preco = float(input('Preço de mais um item: '))
    contador += 1
if credito < preco:
    print(f'Compra do item {contador} negada!')
    
print(f'Itens Comprados: {contador - 1}')
print(f'Total da compra: R$ {total:.2f}')
print(f'Crédito restante: R$ {credito:.2f}')