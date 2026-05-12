def troca(s, i, j):
    s[i], s[j] = s[j], s[i]


def empurra(s, n):
    for i in range(n-1):
        if s[i] > s[i+1]:
            troca(s, i, i+1)


def bubble_sort(s):
    n = len(s)
    while n > 1:
        empurra(s, n)
        n -= 1

# bubble sort não afeta a lista original e sim a cópia
# usa o [:] para fazer uma cópia da lista original

def bubble_sort_2(s):
    lista = s[:]
    n = len(lista)
    while n > 1:
        empurra(lista, n)
        n -= 1

    return lista


lista = [10, 40, 30, 50, 20]

print(bubble_sort_2(lista))
print(lista)
