import math

# def mdc(a: int, b: int) -> int:
# 	a = abs(a)
# 	b = abs(b)
# 	while b != 0:
# 		a, b = b, a % b
# 	return a


# num1 = int(input("Digite o primeiro número: "))
# num2 = int(input("Digite o segundo número: "))
# num3 = int(input("Digite o terceiro número: "))

# resultado = mdc(num1, mdc(num2, num3))
# print("O MDC dos 3 números é:", resultado)


# ========== FORÇA GRAVITACIONAL ==========
def forca_gravitacional(m1: float, m2: float, distancia: float) -> float:
    """
    Calcula a força gravitacional entre dois corpos usando a Lei de Newton.

    F = G * (m1 * m2) / d²

    Args:
            m1: Massa do primeiro corpo (em kg)
            m2: Massa do segundo corpo (em kg)
            distancia: Distância entre os centros dos corpos (em metros)

    Returns:
            Força gravitacional em Newtons (N)
    """
    G = 6.674e-11  # Constante gravitacional universal (N⋅m²/kg²)

    if distancia == 0:
        raise ValueError("A distância não pode ser zero!")

    forca = G * (m1 * m2) / (distancia**2)
    return forca


print("\n" + "=" * 50)
print("CÁLCULO DA FORÇA GRAVITACIONAL")
print("=" * 50)

massa1 = float(input("Digite a massa do primeiro corpo (kg): "))
massa2 = float(input("Digite a massa do segundo corpo (kg): "))
dist = float(input("Digite a distância entre os corpos (m): "))

forca = forca_gravitacional(massa1, massa2, dist)
print(f"\nA força gravitacional entre os corpos é: {forca:.2e} N")


# ========== EQUAÇÃO DO SEGUNDO GRAU ==========


def equacao_segundo_grau(a: float, b: float, c: float):
    """
    Resolve uma equação do segundo grau: ax² + bx + c = 0

    Args:
            a: Coeficiente de x²
            b: Coeficiente de x
            c: Termo independente

    Returns:
            Tuple com as raízes (x1, x2) ou None se não houver raízes reais
    """
    # Verifica se é equação do segundo grau
    if a == 0:
        print("Não é equação do segundo grau (a = 0)")
        return None

    # Calcula delta (Δ = b² - 4ac)
    delta = (b**2) - (4 * a * c)

    # Verifica se existem raízes reais
    if delta < 0:
        print("Não existem raízes reais (Delta < 0)")
        return None

    # Calcula as raízes
    x1 = (-b - math.sqrt(delta)) / (2 * a)
    x2 = (-b + math.sqrt(delta)) / (2 * a)

    return x1, x2


print("\n" + "=" * 50)
print("EQUAÇÃO DO SEGUNDO GRAU: ax² + bx + c = 0")
print("=" * 50)

a = float(input("Digite o coeficiente a: "))
b = float(input("Digite o coeficiente b: "))
c = float(input("Digite o coeficiente c: "))

resultado = equacao_segundo_grau(a, b, c)

if resultado:
    x1, x2 = resultado
    print(f"\nRaízes da equação:")
    print(f"x₁ = {x1:.4f}")
    print(f"x₂ = {x2:.4f}")

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
