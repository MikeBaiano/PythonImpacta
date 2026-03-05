# nome = str(input())
# fixSalary = float(input())
# sales = float(input())

# totalSalary = fixSalary + sales * 0.15

# print(f'TOTAL = R$ {totalSalary:.2f}')

notas = input().split()

N1 = float(notas[0])
N2 = float(notas[1])
N3 = float(notas[2])
N4 = float(notas[3])

Media = (N1 * 2 + N2 * 3 + N3 * 4 + N4 * 1)/10

if 5 <= Media < 7:
    print(f'Media: {Media:.1f}')
    print('Aluno em exame.')
    E = float(input())
    print(f'Nota do exame: {E:.1f}')
    Mf = (E + Media)/2
    if Mf >= 5:
        print('Aluno aprovado.')
    else:
        print('Aluno reprovado.')
    print(f'Media Final: {Mf:.1f}')

if Media >= 7:
    print(f'Media: {Media:.1f}')
    print('Aluno aprovado.')
    
if Media < 5:
    print(f'Media: {Media:.1f}')
    print('Aluno reprovado.')