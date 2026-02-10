# Algoritmo para calcular a soma de 1 até N usando estrutura de repetição Enquanto

# Solicita ao usuário um número inteiro positivo
N = int(input("Digite um número inteiro positivo N: "))

# Inicializa as variáveis
contador = 1
soma = 0

# Estrutura de repetição Enquanto (while)
while contador <= N:
    soma = soma + contador
    contador = contador + 1

# Exibe o resultado
print("A soma de todos os números de 1 até", N, "é:", soma)
