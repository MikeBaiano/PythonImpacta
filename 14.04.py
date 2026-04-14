def dividir_numeros():
    try:
        # Tenta converter a entrada do usuário para inteiro.
        # Pode gerar um ValueError se o usuário digitar letras ou símbolos.
        numerador = int(input("Digite o numerador: "))
        denominador = int(input("Digite o denominador: "))

        # Tenta realizar a divisão.
        # Pode gerar um ZeroDivisionError se o denominador for 0.
        resultado = numerador / denominador

        print(f"O resultado da divisão é: {resultado}")

    # 1. Tratamento MAIS ESPECÍFICO (Filhas da ArithmeticError e ValueError)
    except ValueError:
        print("Erro de Valor: Você deve digitar números inteiros válidos, não letras!")

    except ZeroDivisionError:
        print("Erro Matemático: Não é possível dividir um número por zero!")

    # 2. Tratamento GENÉRICO (O Tronco Principal)
    except Exception as e:
        # Isso vai capturar qualquer outro erro de código que não prevemos acima
        # (ex: um NameError ou TypeError não esperado).
        print(f"Ocorreu um erro inesperado: {e}")

# Executa o programa
# print("--- Calculadora de Divisao ---")
# dividir_numeros()

def dividir():
    try:
        a = float(input("Digite um número: "))
        b = float(input("Digite outro número: "))
        resultado = a / b
    except ValueError:
        print("Erro: Você deve digitar um número.")
    except ZeroDivisionError:
        print("Erro: Divisão por zero não é permitida.")
    else:
        print(resultado)
    finally:
        print("Fim da execução.")

# print(dividir(10, 2))
# dividir(10, 2)
# dividir()

def converter_para_int(valor):
    try:
        num = int(valor)
    except ValueError:
        print(f"Erro: '{valor}' não é um número inteiro válido.")
    else:
        print(f"Conversão bem-sucedida! Número: {num}")
    finally:
        print("Tentativa de conversão encerrada.\n")

# Testes
# converter_para_int("42")
# converter_para_int("abc")

def calculadora_segura():
    while True:
        try:
            n1 = float(input('N1: '))
            n2 = float(input('N2: '))
            op = input('+ - * / ou 0-sair: ')
            
            if op == '0': 
                break

            if op == '+': 
                print(n1 + n2)
            elif op == '-': 
                print(n1 - n2)
            elif op == '*': 
                print(n1 * n2)
            elif op == '/': 
                print(n1 / n2)
            else: 
                print('Operação inválida')

        except ValueError:
            print('Digite números!')
        except ZeroDivisionError:
            print('Não divide por zero!')

# Programa NUNCA quebra!
# calculadora_segura()

def divisao_validada():
    while True:
        try:
            # 1. Peça dois números ao usuário
            num1 = float(input("Digite o primeiro número (numerador): "))
            num2 = float(input("Digite o segundo número (denominador): "))
            
            # 2. Calcule e exiba a divisão
            resultado = num1 / num2
            print(f"\n✅ Sucesso! O resultado de {num1} / {num2} é: {resultado}")
            
            # Se chegou aqui sem erro, quebra o loop
            break 
            
        # 3. Trate ValueError (entrada não numérica)
        except ValueError:
            print("❌ Erro: Entrada inválida! Por favor, digite apenas números.")
            
        # 4. Trate ZeroDivisionError (divisão por zero)
        except ZeroDivisionError:
            print("❌ Erro: Não é possível dividir por zero! Tente outros números.")
            
        print("Tente novamente...\n")

# Execução do programa
print("--- Validação de Divisão ---")
divisao_validada()

