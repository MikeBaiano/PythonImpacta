# ========== SISTEMA DE NOTAS COM SUPABASE ==========
# Sistema de gerenciamento de alunos com persistência no banco de dados Supabase

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Verifica se as credenciais foram configuradas
if not SUPABASE_URL or not SUPABASE_KEY or SUPABASE_URL == "sua_url_do_supabase_aqui":
    print("\n" + "=" * 60)
    print("⚠ ATENÇÃO: Configure suas credenciais do Supabase!")
    print("=" * 60)
    print("\n1. Acesse seu projeto no Supabase")
    print("2. Vá em Settings > API")
    print("3. Copie a URL e a anon/public key")
    print("4. Edite o arquivo .env e cole suas credenciais\n")
    print("Exemplo:")
    print("SUPABASE_URL=https://xxxxx.supabase.co")
    print("SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI...")
    print("=" * 60)
    input("\nPressione ENTER para sair...")
    exit()

# Inicializa o cliente Supabase
try:
    # Remove o tipo hint que pode causar problemas
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ Conectado ao Supabase com sucesso!")
except Exception as e:
    print(f"✗ Erro ao conectar ao Supabase: {e}")
    print("\n💡 Possíveis soluções:")
    print("1. Verifique se as credenciais no arquivo .env estão corretas")
    print("2. Tente: python -m pip install --upgrade supabase")
    print("3. Ou instale uma versão específica: python -m pip install supabase==2.0.3")
    input("\nPressione ENTER para sair...")
    exit()

# Nome da tabela no Supabase
TABELA_ALUNOS = "alunos"


def adicionar_aluno():
    """Adiciona um novo aluno no banco de dados"""
    print("\n--- ADICIONAR ALUNO ---")
    nome = input("Nome do aluno: ").strip()

    if not nome:
        print("✗ Nome não pode ser vazio!")
        return

    try:
        # Solicita as 3 notas
        nota1 = float(input("Nota 1 (0-10): "))
        nota2 = float(input("Nota 2 (0-10): "))
        nota3 = float(input("Nota 3 (0-10): "))

        # Valida as notas
        if not all(0 <= nota <= 10 for nota in [nota1, nota2, nota3]):
            print("✗ As notas devem estar entre 0 e 10!")
            return

        # Calcula a média
        media = round((nota1 + nota2 + nota3) / 3, 2)

        # Define a situação do aluno
        if media >= 7.0:
            situacao = "Aprovado"
        elif media >= 5.0:
            situacao = "Recuperação"
        else:
            situacao = "Reprovado"

        # Insere no banco de dados
        dados = {
            "nome": nome,
            "nota1": nota1,
            "nota2": nota2,
            "nota3": nota3,
            "media": media,
            "situacao": situacao,
        }

        resultado = supabase.table(TABELA_ALUNOS).insert(dados).execute()

        print(f"\n✓ Aluno '{nome}' cadastrado com sucesso!")
        print(f"  Média: {media:.2f} - {situacao}")

    except ValueError:
        print("✗ Erro: Digite valores numéricos válidos para as notas!")
    except Exception as e:
        print(f"✗ Erro ao adicionar aluno: {e}")


def listar_alunos():
    """Lista todos os alunos do banco de dados"""
    try:
        # Busca todos os alunos, ordenados por nome
        resultado = supabase.table(TABELA_ALUNOS).select("*").order("nome").execute()
        alunos = resultado.data

        if not alunos:
            print("\n⚠ Nenhum aluno cadastrado!")
            return

        print("\n" + "=" * 70)
        print(f"LISTA DE ALUNOS (Total: {len(alunos)})")
        print("=" * 70)

        for i, aluno in enumerate(alunos, 1):
            print(f"\n{i}. {aluno['nome']} (ID: {aluno['id']})")
            print(
                f"   Notas: {aluno['nota1']:.1f} | {aluno['nota2']:.1f} | {aluno['nota3']:.1f}"
            )
            print(f"   Média: {aluno['media']:.2f}")
            print(f"   Situação: {aluno['situacao']}")
            print("-" * 70)

    except Exception as e:
        print(f"✗ Erro ao listar alunos: {e}")


def buscar_aluno():
    """Busca um aluno pelo nome"""
    try:
        nome_busca = input("\nDigite o nome do aluno: ").strip()

        if not nome_busca:
            print("✗ Nome não pode ser vazio!")
            return

        # Busca alunos cujo nome contenha o texto buscado (case-insensitive)
        resultado = (
            supabase.table(TABELA_ALUNOS)
            .select("*")
            .ilike("nome", f"%{nome_busca}%")
            .execute()
        )
        alunos = resultado.data

        if not alunos:
            print(f"✗ Nenhum aluno encontrado com '{nome_busca}'")
            return

        print("\n" + "=" * 70)
        print(f"RESULTADO DA BUSCA (Encontrados: {len(alunos)})")
        print("=" * 70)

        for aluno in alunos:
            print(f"\nAluno: {aluno['nome']} (ID: {aluno['id']})")
            print(
                f"Notas: {aluno['nota1']:.1f} | {aluno['nota2']:.1f} | {aluno['nota3']:.1f}"
            )
            print(f"Média: {aluno['media']:.2f}")
            print(f"Situação: {aluno['situacao']}")
            print("-" * 70)

    except Exception as e:
        print(f"✗ Erro ao buscar aluno: {e}")


def calcular_estatisticas():
    """Calcula e exibe estatísticas da turma"""
    try:
        # Busca todos os alunos
        resultado = supabase.table(TABELA_ALUNOS).select("*").execute()
        alunos = resultado.data

        if not alunos:
            print("\n⚠ Nenhum aluno cadastrado!")
            return

        # Conta quantos alunos em cada situação
        aprovados = sum(1 for a in alunos if a["situacao"] == "Aprovado")
        recuperacao = sum(1 for a in alunos if a["situacao"] == "Recuperação")
        reprovados = sum(1 for a in alunos if a["situacao"] == "Reprovado")

        # Calcula média da turma
        soma_medias = sum(float(a["media"]) for a in alunos)
        media_turma = soma_medias / len(alunos)

        # Encontra maior e menor média
        maior_media = max(float(a["media"]) for a in alunos)
        menor_media = min(float(a["media"]) for a in alunos)

        print("\n" + "=" * 70)
        print("ESTATÍSTICAS DA TURMA")
        print("=" * 70)
        print(f"\nTotal de alunos: {len(alunos)}")
        print(f"  • Aprovados: {aprovados} ({aprovados/len(alunos)*100:.1f}%)")
        print(f"  • Recuperação: {recuperacao} ({recuperacao/len(alunos)*100:.1f}%)")
        print(f"  • Reprovados: {reprovados} ({reprovados/len(alunos)*100:.1f}%)")
        print(f"\nMédia da turma: {media_turma:.2f}")
        print(f"Maior média: {maior_media:.2f}")
        print(f"Menor média: {menor_media:.2f}")
        print("=" * 70)

    except Exception as e:
        print(f"✗ Erro ao calcular estatísticas: {e}")


def atualizar_aluno():
    """Atualiza as notas de um aluno"""
    try:
        # Primeiro, lista os alunos para o usuário escolher
        resultado = (
            supabase.table(TABELA_ALUNOS).select("id, nome").order("nome").execute()
        )
        alunos = resultado.data

        if not alunos:
            print("\n⚠ Nenhum aluno cadastrado!")
            return

        print("\n--- ALUNOS CADASTRADOS ---")
        for aluno in alunos:
            print(f"ID {aluno['id']}: {aluno['nome']}")

        aluno_id = int(input("\nDigite o ID do aluno para atualizar: "))

        # Busca o aluno pelo ID
        resultado = (
            supabase.table(TABELA_ALUNOS).select("*").eq("id", aluno_id).execute()
        )

        if not resultado.data:
            print("✗ Aluno não encontrado!")
            return

        aluno = resultado.data[0]
        print(f"\nAtualizando notas de: {aluno['nome']}")
        print(
            f"Notas atuais: {aluno['nota1']:.1f} | {aluno['nota2']:.1f} | {aluno['nota3']:.1f}"
        )

        # Solicita as novas notas
        nota1 = float(input("Nova Nota 1 (0-10): "))
        nota2 = float(input("Nova Nota 2 (0-10): "))
        nota3 = float(input("Nova Nota 3 (0-10): "))

        # Valida as notas
        if not all(0 <= nota <= 10 for nota in [nota1, nota2, nota3]):
            print("✗ As notas devem estar entre 0 e 10!")
            return

        # Calcula nova média e situação
        media = round((nota1 + nota2 + nota3) / 3, 2)

        if media >= 7.0:
            situacao = "Aprovado"
        elif media >= 5.0:
            situacao = "Recuperação"
        else:
            situacao = "Reprovado"

        # Atualiza no banco
        dados_atualizacao = {
            "nota1": nota1,
            "nota2": nota2,
            "nota3": nota3,
            "media": media,
            "situacao": situacao,
        }

        supabase.table(TABELA_ALUNOS).update(dados_atualizacao).eq(
            "id", aluno_id
        ).execute()

        print(f"\n✓ Aluno '{aluno['nome']}' atualizado com sucesso!")
        print(f"  Nova média: {media:.2f} - {situacao}")

    except ValueError:
        print("✗ Erro: Digite valores válidos!")
    except Exception as e:
        print(f"✗ Erro ao atualizar aluno: {e}")


def excluir_aluno():
    """Exclui um aluno do banco de dados"""
    try:
        # Lista os alunos
        resultado = (
            supabase.table(TABELA_ALUNOS).select("id, nome").order("nome").execute()
        )
        alunos = resultado.data

        if not alunos:
            print("\n⚠ Nenhum aluno cadastrado!")
            return

        print("\n--- ALUNOS CADASTRADOS ---")
        for aluno in alunos:
            print(f"ID {aluno['id']}: {aluno['nome']}")

        aluno_id = int(input("\nDigite o ID do aluno para excluir: "))

        # Busca o aluno
        resultado = (
            supabase.table(TABELA_ALUNOS).select("*").eq("id", aluno_id).execute()
        )

        if not resultado.data:
            print("✗ Aluno não encontrado!")
            return

        aluno = resultado.data[0]

        # Confirmação
        confirmacao = input(
            f"\n⚠ Tem certeza que deseja excluir '{aluno['nome']}'? (s/n): "
        )

        if confirmacao.lower() == "s":
            supabase.table(TABELA_ALUNOS).delete().eq("id", aluno_id).execute()
            print(f"✓ Aluno '{aluno['nome']}' excluído com sucesso!")
        else:
            print("✗ Exclusão cancelada!")

    except ValueError:
        print("✗ Erro: Digite um ID válido!")
    except Exception as e:
        print(f"✗ Erro ao excluir aluno: {e}")


# ========== MENU PRINCIPAL ==========
def menu_principal():
    """Menu interativo do sistema"""

    while True:
        print("\n" + "=" * 70)
        print("SISTEMA DE NOTAS - SUPABASE")
        print("=" * 70)
        print("1. Adicionar Aluno")
        print("2. Listar Todos os Alunos")
        print("3. Buscar Aluno por Nome")
        print("4. Atualizar Notas de Aluno")
        print("5. Excluir Aluno")
        print("6. Estatísticas da Turma")
        print("0. Sair")
        print("=" * 70)

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            adicionar_aluno()
        elif opcao == "2":
            listar_alunos()
        elif opcao == "3":
            buscar_aluno()
        elif opcao == "4":
            atualizar_aluno()
        elif opcao == "5":
            excluir_aluno()
        elif opcao == "6":
            calcular_estatisticas()
        elif opcao == "0":
            print("\n✓ Encerrando sistema... Até logo!")
            break
        else:
            print("\n✗ Opção inválida! Tente novamente.")


# Executa o sistema
if __name__ == "__main__":
    menu_principal()
