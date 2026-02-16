# -*- coding: utf-8 -*-

"""
Bem-vindo ao seu assistente de codificação Python!
Este programa foi projetado para ajudá-lo a praticar e reaprender os conceitos básicos de Python.
Sinta-se à vontade para modificar e experimentar cada parte do código.
"""

# --- 1. Variáveis e Tipos de Dados ---
# Em Python, você não precisa declarar o tipo de uma variável.
# O interpretador infere o tipo com base no valor atribuído.

# String (texto)
nome = "Mundo"
print(f"Olá, {nome}!")  # Usando f-string para formatar a saída

# Integer (número inteiro)
idade = 25
print(f"Idade: {idade}")

# Float (número com ponto flutuante)
altura = 1.75
print(f"Altura: {altura}")

# Boolean (verdadeiro ou falso)
gosta_de_python = True
print(f"Gosta de Python? {gosta_de_python}")

# List (lista mutável de itens)
frutas = ["maçã", "banana", "laranja"]
print(f"Lista de frutas: {frutas}")
frutas.append("morango")  # Adicionando um item à lista
print(f"Lista de frutas atualizada: {frutas}")

# Dictionary (dicionário de pares chave-valor)
pessoa = {"nome": "Carlos", "idade": 30, "cidade": "São Paulo"}
print(f"Dados da pessoa: {pessoa}")
print(f"Idade de {pessoa['nome']}: {pessoa['idade']}")


# --- 2. Funções ---
# Funções são blocos de código reutilizáveis. Elas ajudam a organizar o seu programa.


def saudacao(nome_pessoa):
    """
    Esta é uma docstring. Ela explica o que a função faz.
    Esta função recebe um nome e retorna uma saudação.
    """
    return f"Olá, {nome_pessoa}! Seja bem-vindo(a) de volta ao Python."


# Chamando a função e imprimindo o resultado
mensagem = saudacao("Alex")
print(mensagem)


# --- 3. Estruturas de Controle ---
# Elas permitem que você controle o fluxo de execução do seu código.


# if, elif, else (condicionais)
def verificar_idade(idade_pessoa):
    if idade_pessoa < 18:
        return "Menor de idade"
    elif 18 <= idade_pessoa < 60:
        return "Adulto"
    else:
        return "Idoso"


status_idade = verificar_idade(30)
print(f"Status de idade (30 anos): {status_idade}")
status_idade_jovem = verificar_idade(15)
print(f"Status de idade (15 anos): {status_idade_jovem}")


# for loop (para iterar sobre sequências)
print("Iterando sobre a lista de frutas:")
for fruta in frutas:
    print(f"- {fruta.capitalize()}")  # .capitalize() torna a primeira letra maiúscula

# while loop (executa enquanto uma condição for verdadeira)
print("Contagem regressiva com while:")
contador = 5
while contador > 0:
    print(contador)
    contador -= 1  # O mesmo que contador = contador - 1
print("Fogo!")


# --- 4. Próximos Passos ---
# Agora é sua vez! Tente criar suas próprias funções ou modificar as existentes.
# Por exemplo, crie uma função que receba uma lista de números e retorne a soma de todos eles.
# Ou modifique a função `verificar_idade` para incluir mais faixas etárias.


# Exemplo de desafio:
def somar_lista(numeros):
    # Escreva o código aqui para somar os números na lista e retornar o total.
    total = 0
    for numero in numeros:
        total += numero
    return total


# Teste sua função
meus_numeros = [10, 20, 30, 40]
soma_total = somar_lista(meus_numeros)
print(f"A soma dos números {meus_numeros} é: {soma_total}")

print("Estudo feliz!")
