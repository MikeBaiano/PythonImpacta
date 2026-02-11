# ========== SISTEMA DE NOTAS DE ALUNOS ==========
# Programa para cadastrar alunos e calcular médias

# Lista para armazenar os alunos (inicialmente vazia)
alunos = []


def adicionar_aluno():
    """Adiciona um novo aluno com suas notas"""
    print("\n--- ADICIONAR ALUNO ---")
    nome = input("Nome do aluno: ")

    # Solicita as 3 notas
    nota1 = float(input("Nota 1: "))
    nota2 = float(input("Nota 2: "))
    nota3 = float(input("Nota 3: "))

    # Calcula a média
    media = (nota1 + nota2 + nota3) / 3

    # Define a situação do aluno
    if media >= 7.0:
        situacao = "Aprovado"
    elif media >= 5.0:
        situacao = "Recuperação"
    else:
        situacao = "Reprovado"

    # Cria um dicionário com os dados do aluno
    aluno = {
        "nome": nome,
        "nota1": nota1,
        "nota2": nota2,
        "nota3": nota3,
        "media": media,
        "situacao": situacao,
    }

    # Adiciona o aluno à lista
    alunos.append(aluno)
    print(f"✓ Aluno {nome} cadastrado com média {media:.2f} - {situacao}")


def listar_alunos():
    """Lista todos os alunos cadastrados"""
    if len(alunos) == 0:
        print("\n⚠ Nenhum aluno cadastrado!")
        return

    print("\n" + "=" * 60)
    print("LISTA DE ALUNOS")
    print("=" * 60)

    for i, aluno in enumerate(alunos, 1):
        print(f"\n{i}. {aluno['nome']}")
        print(
            f"   Notas: {aluno['nota1']:.1f} | {aluno['nota2']:.1f} | {aluno['nota3']:.1f}"
        )
        print(f"   Média: {aluno['media']:.2f}")
        print(f"   Situação: {aluno['situacao']}")
        print("-" * 60)


def calcular_estatisticas():
    """Calcula e exibe estatísticas da turma"""
    if len(alunos) == 0:
        print("\n⚠ Nenhum aluno cadastrado!")
        return

    # Conta quantos alunos em cada situação
    aprovados = 0
    recuperacao = 0
    reprovados = 0
    soma_medias = 0

    for aluno in alunos:
        soma_medias += aluno["media"]

        if aluno["situacao"] == "Aprovado":
            aprovados += 1
        elif aluno["situacao"] == "Recuperação":
            recuperacao += 1
        else:
            reprovados += 1

    media_turma = soma_medias / len(alunos)

    print("\n" + "=" * 60)
    print("ESTATÍSTICAS DA TURMA")
    print("=" * 60)
    print(f"Total de alunos: {len(alunos)}")
    print(f"Aprovados: {aprovados}")
    print(f"Recuperação: {recuperacao}")
    print(f"Reprovados: {reprovados}")
    print(f"\nMédia da turma: {media_turma:.2f}")


def buscar_aluno():
    """Busca um aluno pelo nome"""
    if len(alunos) == 0:
        print("\n⚠ Nenhum aluno cadastrado!")
        return

    nome_busca = input("\nDigite o nome do aluno: ")

    encontrado = False
    for aluno in alunos:
        if nome_busca.lower() in aluno["nome"].lower():
            print("\n" + "=" * 60)
            print(f"Aluno: {aluno['nome']}")
            print(
                f"Notas: {aluno['nota1']:.1f} | {aluno['nota2']:.1f} | {aluno['nota3']:.1f}"
            )
            print(f"Média: {aluno['media']:.2f}")
            print(f"Situação: {aluno['situacao']}")
            print("=" * 60)
            encontrado = True

    if not encontrado:
        print("✗ Aluno não encontrado!")


# ========== MENU PRINCIPAL ==========
while True:
    print("\n" + "=" * 60)
    print("SISTEMA DE NOTAS DE ALUNOS")
    print("=" * 60)
    print("1. Adicionar Aluno")
    print("2. Listar Todos os Alunos")
    print("3. Buscar Aluno")
    print("4. Estatísticas da Turma")
    print("0. Sair")
    print("=" * 60)

    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        adicionar_aluno()
    elif opcao == "2":
        listar_alunos()
    elif opcao == "3":
        buscar_aluno()
    elif opcao == "4":
        calcular_estatisticas()
    elif opcao == "0":
        print("\n✓ Encerrando sistema... Até logo!")
        break
    else:
        print("\n✗ Opção inválida! Tente novamente.")
