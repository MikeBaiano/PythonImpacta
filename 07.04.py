# credito = float(input('Seu crédito: '))
# contador = 0
# while credito >= 0:
#     item = float(input('Preço do item: '))
#     if item > credito:
#         print('Compra negada! Ultrapassou o crédito!')
#         break
#     contador += 1
#     credito -= item
#     print(f'Crédito restante: R$ {credito:.2f}')
# print(f'Crédito após compras: R$ {credito:.2f}')
# print(f'Você comprou {contador} itens!')

# def invertido(n):
#     n = str(n)
#     return n[::-1]

# print(invertido(12345))

# def invertido(n):
#     while True:
#         print( n % 10, end = '' )
#         n = n//10
#         if n == 0:
#             break

# print(invertido(12345))

def tabuleiro(n):
    linha = 0
    while linha < n:
        coluna = 0
        while coluna < n:
            if(coluna + linha) % 2 == 0:
                print(2 * chr(9608), end = '')
            else:
                print(2 * ' ', end = '')
            coluna += 1
        print()
        linha += 1

tabuleiro(5)