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

def par_impar(n):
    if n % 2 == 0:
        return "Sim"
    else:
        return "Não"



print(f'{10} é par? {par_impar(10)}')
print(f'{11} é par? {par_impar(11)}')

print(f'O valor de pi é {mt.pi:.200f}')
