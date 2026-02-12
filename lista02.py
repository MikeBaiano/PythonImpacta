# Questão 1: Cálculo de Área de Trapézio
# Algoritmo que calcula a área de um trapézio usando a fórmula A = (B + b) * h / 2

print("=== Cálculo da Área de um Trapézio ===")
print()

# Entrada de dados - leitura das variáveis
B = float(input("Digite a base maior (B): "))
b = float(input("Digite a base menor (b): "))
h = float(input("Digite a altura (h): "))

# Processamento - cálculo da área
A = (B + b) * h / 2

# Saída - exibição do resultado
print()
print(f"A área do trapézio é: {A}")
