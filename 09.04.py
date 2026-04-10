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


# Números perfeitos 1164
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
        if (
            x % divisor == 0
        ):  # Verifica se o resto da divisão é 0 (ou seja, se é um divisor exato)
            soma_divisores += divisor

        divisor += 1  # Passamos para o próximo divisor para ir testando

    # Quando o laço de dentro acaba, a gente verifica se a soma deu o próprio número x
    if soma_divisores == x:
        print(f"{x} eh perfeito")
    else:
        print(f"{x} nao eh perfeito")

    # E então não podemos esquecer de contabilizar que lemos mais um caso!
    caso_atual += 1

# Números primos 1165
n_casos = int(input())
caso_atual = 0

while caso_atual < n_casos:
    x = int(input())

    qtd_divisores = 0

    i = 1

    while i <= x:
        if x % i == 0:
            qtd_divisores += 1
        i += 1

    if qtd_divisores == 2:
        print(f"{x} eh primo")
    else:
        print(f"{x} nao eh primo")

    caso_atual += 1

# Dígitos Diferentes 1285
while True:
    try:
        # Lemos os dois valores na mesma linha
        entrada = input().split()
        if not entrada:
            break
        
        n = int(entrada[0])
        m = int(entrada[1])
        
        casas_validas = 0
        
        # Testamos cada casa no intervalo de [N, M]
        atual = n
        while atual <= m:
            # str(atual) transforma o número em texto, por ex: "838"
            # set( str(atual) ) cria um conjunto dos caracteres. ex: {'8', '3'}
            # Como um "set" não aceita itens duplicados, nós sabemos que 
            # não tem repetição se o set tiver o mesmo tamanho da string!
            if len(str(atual)) == len(set(str(atual))):
                casas_validas += 1
            
            atual += 1
            
        print(casas_validas)
        
    except EOFError:
        # Quando o beecrowd não tiver mais casos de testes para enviar, 
        # a função input() lança esse erro (Fim de Arquivo), e nosso código para.
        break

# Feedback 1546
# Você tem razão! A lógica desse é muito simpes, a única "dificuldade" é 
# que ele tem UM LAÇO DENTRO DE OUTRO LAÇO, porque os dados são agrupados por dia.

n_casos = int(input())
caso_atual = 0

# Para economizar vários 'if / elif' gigantes, podemos usar a estrutura
# de Dicionário em Python! (Mapeia a CHAVE 1 -> para o VALOR "Rolien")
responsaveis = {
    1: "Rolien",
    2: "Naej",
    3: "Elehcim",
    4: "Odranoel"
}

# Laço de Fora: Repete N vezes (uma vez para cada Dia do teste)
while caso_atual < n_casos:
    
    # Quantidade de feedbacks que aquele dia específico teve
    k_feedbacks = int(input())
    feedback_atual = 0
    
    # Laço de Dentro: Repete K vezes (uma vez para cada feedback do dia)
    while feedback_atual < k_feedbacks:
        categoria = int(input())
        
        # Aqui é a mágica do Dicionário: Passamos o número, ele retorna o nome pronto!
        print(responsaveis[categoria])
        
        feedback_atual += 1
        
    caso_atual += 1
