# ========== SISTEMA DE GERENCIAMENTO DE BIBLIOTECA ==========
# Sistema completo com livros, membros e empréstimos usando Supabase
# Conceitos: datetime, relacionamentos, validações, relatórios

import os
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from supabase import create_client

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
    input("\nPressione ENTER para sair...")
    exit()

# Inicializa o cliente Supabase
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✓ Conectado ao Supabase com sucesso!")
except Exception as e:
    print(f"✗ Erro ao conectar ao Supabase: {e}")
    input("\nPressione ENTER para sair...")
    exit()

# Nomes das tabelas no Supabase
TABELA_LIVROS = "livros"
TABELA_MEMBROS = "membros"
TABELA_EMPRESTIMOS = "emprestimos"

# Constantes do sistema
LIMITE_EMPRESTIMOS = 3  # Máximo de empréstimos ativos por membro
PRAZO_ESTUDANTE = 7  # Dias de empréstimo para estudante
PRAZO_PROFESSOR = 14  # Dias de empréstimo para professor
MULTA_POR_DIA = 1.00  # R$ por dia de atraso
GENEROS_VALIDOS = [
    "Romance",
    "Ficção Científica",
    "Fantasia",
    "Terror",
    "Biografia",
    "História",
    "Ciência",
    "Tecnologia",
    "Autoajuda",
    "Educação",
    "Infantil",
    "Outro",
]


# ========== FUNÇÕES DE VALIDAÇÃO ==========
def validar_email(email):
    """
    Valida se o email tem um formato básico válido.
    Usa verificação simples com 'in' e split — sem regex.
    """
    if "@" not in email or "." not in email:
        return False
    partes = email.split("@")
    if len(partes) != 2:
        return False
    usuario, dominio = partes
    if len(usuario) == 0 or len(dominio) < 3:
        return False
    if "." not in dominio:
        return False
    return True


def validar_telefone(telefone):
    """Valida se o telefone contém apenas dígitos e tem entre 10-11 caracteres"""
    apenas_digitos = (
        telefone.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")
    )
    return apenas_digitos.isdigit() and 10 <= len(apenas_digitos) <= 11


def formatar_data(data_str):
    """Converte string de data ISO (YYYY-MM-DD) para formato brasileiro (DD/MM/YYYY)"""
    try:
        # Trata tanto date quanto string
        if isinstance(data_str, date):
            return data_str.strftime("%d/%m/%Y")
        data_obj = datetime.strptime(str(data_str), "%Y-%m-%d")
        return data_obj.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return str(data_str) if data_str else "N/A"


def calcular_dias_atraso(data_devolucao_prevista_str):
    """
    Calcula quantos dias de atraso existem a partir da data prevista de devolução.
    Retorna 0 se não estiver atrasado.
    """
    try:
        data_prevista = datetime.strptime(
            str(data_devolucao_prevista_str), "%Y-%m-%d"
        ).date()
        hoje = date.today()
        diferenca = (hoje - data_prevista).days
        return max(0, diferenca)  # max() garante que não retorna valor negativo
    except (ValueError, TypeError):
        return 0


# ========== FUNÇÕES DE LIVROS ==========
def cadastrar_livro():
    """Cadastra um novo livro no banco de dados"""
    print("\n" + "=" * 60)
    print("📚 CADASTRAR NOVO LIVRO")
    print("=" * 60)

    titulo = input("Título do livro: ").strip()
    if not titulo:
        print("✗ Título não pode ser vazio!")
        return

    autor = input("Autor: ").strip()
    if not autor:
        print("✗ Autor não pode ser vazio!")
        return

    # Mostra os gêneros disponíveis usando enumerate()
    print("\nGêneros disponíveis:")
    for i, genero in enumerate(GENEROS_VALIDOS, 1):
        print(f"  {i:2d}. {genero}")

    try:
        opcao_genero = int(input("\nEscolha o número do gênero: "))
        if not 1 <= opcao_genero <= len(GENEROS_VALIDOS):
            print("✗ Opção de gênero inválida!")
            return
        genero = GENEROS_VALIDOS[opcao_genero - 1]  # -1 porque lista começa em 0

    except ValueError:
        print("✗ Digite um número válido!")
        return

    try:
        ano = int(input("Ano de publicação: "))
        ano_atual = datetime.now().year
        if not 1450 <= ano <= ano_atual:
            print(f"✗ Ano deve estar entre 1450 e {ano_atual}!")
            return

        quantidade = int(input("Quantidade de cópias (padrão=1): ") or "1")
        if quantidade < 1:
            print("✗ Quantidade deve ser pelo menos 1!")
            return

    except ValueError:
        print("✗ Digite valores numéricos válidos!")
        return

    try:
        dados = {
            "titulo": titulo,
            "autor": autor,
            "genero": genero,
            "ano_publicacao": ano,
            "quantidade_total": quantidade,
            "quantidade_disponivel": quantidade,
        }

        resultado = supabase.table(TABELA_LIVROS).insert(dados).execute()

        print(f"\n✓ Livro '{titulo}' cadastrado com sucesso!")
        print(f"  Autor: {autor} | Gênero: {genero} | Ano: {ano}")
        print(f"  Cópias: {quantidade}")

    except Exception as e:
        print(f"✗ Erro ao cadastrar livro: {e}")


def listar_livros():
    """Lista todos os livros do banco de dados"""
    try:
        resultado = supabase.table(TABELA_LIVROS).select("*").order("titulo").execute()
        livros = resultado.data

        if not livros:
            print("\n⚠ Nenhum livro cadastrado!")
            return

        print("\n" + "=" * 80)
        print(f"📚 ACERVO DA BIBLIOTECA (Total: {len(livros)} títulos)")
        print("=" * 80)

        # Cabeçalho da tabela formatada
        print(f"\n{'ID':<5} {'Título':<30} {'Autor':<20} {'Gênero':<15} {'Disp.':<6}")
        print("-" * 80)

        for livro in livros:
            # Trunca strings longas para manter formatação da tabela
            titulo = (
                livro["titulo"][:28] + ".."
                if len(livro["titulo"]) > 30
                else livro["titulo"]
            )
            autor = (
                livro["autor"][:18] + ".."
                if len(livro["autor"]) > 20
                else livro["autor"]
            )

            # Indicador visual de disponibilidade
            disp = livro["quantidade_disponivel"]
            total = livro["quantidade_total"]
            indicador = f"{disp}/{total}"

            # Usa cores visuais com emojis
            if disp == 0:
                status = "🔴"
            elif disp < total:
                status = "🟡"
            else:
                status = "🟢"

            print(
                f"{livro['id']:<5} {titulo:<30} {autor:<20} {livro['genero']:<15} {status} {indicador}"
            )

        print("-" * 80)
        print("🟢 Disponível | 🟡 Parcial | 🔴 Indisponível")

    except Exception as e:
        print(f"✗ Erro ao listar livros: {e}")


def buscar_livro():
    """Busca livros por título ou autor"""
    print("\n" + "=" * 60)
    print("🔍 BUSCAR LIVRO")
    print("=" * 60)
    print("1. Buscar por título")
    print("2. Buscar por autor")
    print("3. Buscar por gênero")

    opcao = input("\nEscolha: ").strip()
    termo = input("Digite o termo de busca: ").strip()

    if not termo:
        print("✗ Termo de busca não pode ser vazio!")
        return

    try:
        # Usa um dicionário para mapear opção ao campo — mais elegante que if/elif
        campo_busca = {"1": "titulo", "2": "autor", "3": "genero"}

        if opcao not in campo_busca:
            print("✗ Opção inválida!")
            return

        campo = campo_busca[opcao]

        resultado = (
            supabase.table(TABELA_LIVROS)
            .select("*")
            .ilike(campo, f"%{termo}%")
            .execute()
        )
        livros = resultado.data

        if not livros:
            print(f"✗ Nenhum livro encontrado com '{termo}'")
            return

        print(f"\n✓ Encontrados: {len(livros)} livro(s)")
        print("-" * 60)

        for livro in livros:
            print(f"\n  📖 {livro['titulo']} (ID: {livro['id']})")
            print(f"     Autor: {livro['autor']}")
            print(f"     Gênero: {livro['genero']} | Ano: {livro['ano_publicacao']}")
            print(
                f"     Disponível: {livro['quantidade_disponivel']}/{livro['quantidade_total']}"
            )

    except Exception as e:
        print(f"✗ Erro ao buscar livro: {e}")


# ========== FUNÇÕES DE MEMBROS ==========
def cadastrar_membro():
    """Cadastra um novo membro da biblioteca"""
    print("\n" + "=" * 60)
    print("👤 CADASTRAR NOVO MEMBRO")
    print("=" * 60)

    nome = input("Nome completo: ").strip()
    if not nome:
        print("✗ Nome não pode ser vazio!")
        return

    email = input("Email: ").strip().lower()
    if not validar_email(email):
        print("✗ Email inválido! Formato esperado: usuario@dominio.com")
        return

    telefone = input("Telefone (ex: 11999998888): ").strip()
    if telefone and not validar_telefone(telefone):
        print("✗ Telefone inválido! Use apenas números (10-11 dígitos)")
        return

    print("\nTipo de membro:")
    print("  1. Estudante (empréstimo de 7 dias)")
    print("  2. Professor (empréstimo de 14 dias)")
    opcao_tipo = input("Escolha: ").strip()

    # Operador ternário — forma compacta de if/else
    tipo = (
        "Estudante" if opcao_tipo == "1" else "Professor" if opcao_tipo == "2" else None
    )

    if tipo is None:
        print("✗ Tipo inválido!")
        return

    try:
        dados = {
            "nome": nome,
            "email": email,
            "telefone": telefone if telefone else None,
            "tipo": tipo,
            "ativo": True,
        }

        resultado = supabase.table(TABELA_MEMBROS).insert(dados).execute()

        prazo = PRAZO_ESTUDANTE if tipo == "Estudante" else PRAZO_PROFESSOR
        print(f"\n✓ Membro '{nome}' cadastrado com sucesso!")
        print(f"  Tipo: {tipo} | Prazo de empréstimo: {prazo} dias")

    except Exception as e:
        # Verifica se é erro de email duplicado
        if "duplicate" in str(e).lower() or "unique" in str(e).lower():
            print(f"✗ Já existe um membro com o email '{email}'!")
        else:
            print(f"✗ Erro ao cadastrar membro: {e}")


def listar_membros():
    """Lista todos os membros e seus empréstimos ativos"""
    try:
        resultado = supabase.table(TABELA_MEMBROS).select("*").order("nome").execute()
        membros = resultado.data

        if not membros:
            print("\n⚠ Nenhum membro cadastrado!")
            return

        print("\n" + "=" * 80)
        print(f"👥 MEMBROS DA BIBLIOTECA (Total: {len(membros)})")
        print("=" * 80)

        for membro in membros:
            # Busca empréstimos ativos deste membro
            emp_resultado = (
                supabase.table(TABELA_EMPRESTIMOS)
                .select("*")
                .eq("membro_id", membro["id"])
                .eq("status", "Ativo")
                .execute()
            )
            emprestimos_ativos = len(emp_resultado.data)

            # Indicador de status do membro
            status_membro = "✅ Ativo" if membro["ativo"] else "❌ Inativo"

            print(f"\n  👤 {membro['nome']} (ID: {membro['id']})")
            print(f"     Email: {membro['email']}")
            print(f"     Telefone: {membro.get('telefone', 'N/A') or 'N/A'}")
            print(f"     Tipo: {membro['tipo']} | Status: {status_membro}")
            print(f"     Empréstimos ativos: {emprestimos_ativos}/{LIMITE_EMPRESTIMOS}")
            print("-" * 80)

    except Exception as e:
        print(f"✗ Erro ao listar membros: {e}")


# ========== FUNÇÕES DE EMPRÉSTIMOS ==========
def realizar_emprestimo():
    """Realiza um novo empréstimo com validações completas"""
    print("\n" + "=" * 60)
    print("📤 REALIZAR EMPRÉSTIMO")
    print("=" * 60)

    try:
        # ---- PASSO 1: Selecionar o membro ----
        membros_result = (
            supabase.table(TABELA_MEMBROS)
            .select("id, nome, tipo, ativo")
            .eq("ativo", True)
            .order("nome")
            .execute()
        )
        membros = membros_result.data

        if not membros:
            print("✗ Nenhum membro ativo cadastrado!")
            return

        print("\nMembros ativos:")
        for m in membros:
            print(f"  ID {m['id']}: {m['nome']} ({m['tipo']})")

        membro_id = int(input("\nDigite o ID do membro: "))

        # Busca o membro selecionado usando list comprehension com next()
        membro = next((m for m in membros if m["id"] == membro_id), None)
        if membro is None:
            print("✗ Membro não encontrado ou inativo!")
            return

        # ---- PASSO 2: Verificar limite de empréstimos ----
        emp_ativos_result = (
            supabase.table(TABELA_EMPRESTIMOS)
            .select("id")
            .eq("membro_id", membro_id)
            .eq("status", "Ativo")
            .execute()
        )
        qtd_emprestimos_ativos = len(emp_ativos_result.data)

        if qtd_emprestimos_ativos >= LIMITE_EMPRESTIMOS:
            print(
                f"✗ Membro '{membro['nome']}' já atingiu o limite de {LIMITE_EMPRESTIMOS} empréstimos ativos!"
            )
            print("  Devolva algum livro antes de realizar novo empréstimo.")
            return

        print(f"\n✓ Membro: {membro['nome']} ({membro['tipo']})")
        print(f"  Empréstimos ativos: {qtd_emprestimos_ativos}/{LIMITE_EMPRESTIMOS}")

        # ---- PASSO 3: Selecionar o livro ----
        livros_result = (
            supabase.table(TABELA_LIVROS)
            .select("id, titulo, autor, quantidade_disponivel")
            .gt("quantidade_disponivel", 0)  # Apenas livros disponíveis
            .order("titulo")
            .execute()
        )
        livros = livros_result.data

        if not livros:
            print("✗ Nenhum livro disponível para empréstimo!")
            return

        print("\nLivros disponíveis:")
        for l in livros:
            print(
                f"  ID {l['id']}: {l['titulo']} - {l['autor']} (Disponível: {l['quantidade_disponivel']})"
            )

        livro_id = int(input("\nDigite o ID do livro: "))

        # Verifica se o livro está na lista de disponíveis
        livro = next((l for l in livros if l["id"] == livro_id), None)
        if livro is None:
            print("✗ Livro não encontrado ou indisponível!")
            return

        # ---- PASSO 4: Verificar se já tem este livro emprestado ----
        ja_emprestado = (
            supabase.table(TABELA_EMPRESTIMOS)
            .select("id")
            .eq("membro_id", membro_id)
            .eq("livro_id", livro_id)
            .eq("status", "Ativo")
            .execute()
        )
        if ja_emprestado.data:
            print(f"✗ Este membro já possui o livro '{livro['titulo']}' emprestado!")
            return

        # ---- PASSO 5: Calcular datas ----
        data_emprestimo = date.today()
        prazo_dias = (
            PRAZO_PROFESSOR if membro["tipo"] == "Professor" else PRAZO_ESTUDANTE
        )
        data_devolucao_prevista = data_emprestimo + timedelta(days=prazo_dias)

        # ---- PASSO 6: Registrar o empréstimo ----
        dados_emprestimo = {
            "livro_id": livro_id,
            "membro_id": membro_id,
            "data_emprestimo": data_emprestimo.isoformat(),
            "data_devolucao_prevista": data_devolucao_prevista.isoformat(),
            "data_devolucao_real": None,
            "status": "Ativo",
            "multa": 0,
        }
        supabase.table(TABELA_EMPRESTIMOS).insert(dados_emprestimo).execute()

        # ---- PASSO 7: Atualizar disponibilidade do livro ----
        nova_quantidade = livro["quantidade_disponivel"] - 1
        supabase.table(TABELA_LIVROS).update(
            {"quantidade_disponivel": nova_quantidade}
        ).eq("id", livro_id).execute()

        print(f"\n{'=' * 60}")
        print("✓ EMPRÉSTIMO REALIZADO COM SUCESSO!")
        print(f"{'=' * 60}")
        print(f"  Membro: {membro['nome']}")
        print(f"  Livro: {livro['titulo']}")
        print(f"  Data do empréstimo: {formatar_data(data_emprestimo)}")
        print(f"  Data de devolução: {formatar_data(data_devolucao_prevista)}")
        print(f"  Prazo: {prazo_dias} dias")

    except ValueError:
        print("✗ Digite um ID válido!")
    except Exception as e:
        print(f"✗ Erro ao realizar empréstimo: {e}")


def devolver_livro():
    """Devolve um livro e calcula multa por atraso se necessário"""
    print("\n" + "=" * 60)
    print("📥 DEVOLVER LIVRO")
    print("=" * 60)

    try:
        # Busca empréstimos ativos
        emp_result = (
            supabase.table(TABELA_EMPRESTIMOS)
            .select("*")
            .eq("status", "Ativo")
            .order("data_devolucao_prevista")
            .execute()
        )
        emprestimos = emp_result.data

        if not emprestimos:
            print("⚠ Nenhum empréstimo ativo no momento!")
            return

        print("\nEmpréstimos ativos:")
        print(
            f"\n{'ID':<5} {'Membro':<20} {'Livro':<25} {'Devolução Prevista':<18} {'Status'}"
        )
        print("-" * 80)

        for emp in emprestimos:
            # Busca nome do membro e título do livro
            membro_res = (
                supabase.table(TABELA_MEMBROS)
                .select("nome")
                .eq("id", emp["membro_id"])
                .execute()
            )
            livro_res = (
                supabase.table(TABELA_LIVROS)
                .select("titulo")
                .eq("id", emp["livro_id"])
                .execute()
            )

            nome_membro = (
                membro_res.data[0]["nome"] if membro_res.data else "Desconhecido"
            )
            titulo_livro = (
                livro_res.data[0]["titulo"] if livro_res.data else "Desconhecido"
            )

            # Trunca para manter formatação
            nome_membro = (
                nome_membro[:18] + ".." if len(nome_membro) > 20 else nome_membro
            )
            titulo_livro = (
                titulo_livro[:23] + ".." if len(titulo_livro) > 25 else titulo_livro
            )

            dias_atraso = calcular_dias_atraso(emp["data_devolucao_prevista"])
            status_texto = (
                f"⚠ {dias_atraso}d atraso" if dias_atraso > 0 else "✓ No prazo"
            )

            print(
                f"{emp['id']:<5} {nome_membro:<20} {titulo_livro:<25} {formatar_data(emp['data_devolucao_prevista']):<18} {status_texto}"
            )

        print("-" * 80)

        emp_id = int(input("\nDigite o ID do empréstimo para devolver: "))

        # Busca o empréstimo selecionado
        emprestimo = next((e for e in emprestimos if e["id"] == emp_id), None)
        if emprestimo is None:
            print("✗ Empréstimo não encontrado!")
            return

        # Calcula multa por atraso
        data_hoje = date.today()
        dias_atraso = calcular_dias_atraso(emprestimo["data_devolucao_prevista"])
        multa = round(dias_atraso * MULTA_POR_DIA, 2)

        # Atualiza o empréstimo
        dados_atualizacao = {
            "data_devolucao_real": data_hoje.isoformat(),
            "status": "Devolvido",
            "multa": multa,
        }
        supabase.table(TABELA_EMPRESTIMOS).update(dados_atualizacao).eq(
            "id", emp_id
        ).execute()

        # Devolve o livro ao estoque (incrementa quantidade_disponivel)
        livro_res = (
            supabase.table(TABELA_LIVROS)
            .select("quantidade_disponivel")
            .eq("id", emprestimo["livro_id"])
            .execute()
        )
        if livro_res.data:
            nova_qtd = livro_res.data[0]["quantidade_disponivel"] + 1
            supabase.table(TABELA_LIVROS).update(
                {"quantidade_disponivel": nova_qtd}
            ).eq("id", emprestimo["livro_id"]).execute()

        # Resultado da devolução
        print(f"\n{'=' * 60}")
        print("✓ LIVRO DEVOLVIDO COM SUCESSO!")
        print(f"{'=' * 60}")
        print(f"  Data de devolução: {formatar_data(data_hoje)}")

        if dias_atraso > 0:
            print(f"\n  ⚠ ATRASO DE {dias_atraso} DIA(S)")
            print(f"  💰 Multa: R$ {multa:.2f} (R$ {MULTA_POR_DIA:.2f}/dia)")
        else:
            print("  ✓ Devolvido dentro do prazo! Sem multa.")

    except ValueError:
        print("✗ Digite um ID válido!")
    except Exception as e:
        print(f"✗ Erro ao devolver livro: {e}")


# ========== RELATÓRIOS ==========
def relatorio_emprestimos():
    """Gera relatório de empréstimos filtrado por status"""
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE EMPRÉSTIMOS")
    print("=" * 60)
    print("1. Todos os empréstimos")
    print("2. Apenas ativos")
    print("3. Apenas devolvidos")
    print("4. Apenas atrasados (ativos com prazo vencido)")

    opcao = input("\nEscolha o filtro: ").strip()

    try:
        # Monta a query base
        query = supabase.table(TABELA_EMPRESTIMOS).select("*")

        if opcao == "2":
            query = query.eq("status", "Ativo")
            titulo_relatorio = "EMPRÉSTIMOS ATIVOS"
        elif opcao == "3":
            query = query.eq("status", "Devolvido")
            titulo_relatorio = "EMPRÉSTIMOS DEVOLVIDOS"
        elif opcao == "4":
            query = query.eq("status", "Ativo")
            titulo_relatorio = "EMPRÉSTIMOS ATRASADOS"
        elif opcao == "1":
            titulo_relatorio = "TODOS OS EMPRÉSTIMOS"
        else:
            print("✗ Opção inválida!")
            return

        resultado = query.order("created_at", desc=True).execute()
        emprestimos = resultado.data

        if not emprestimos:
            print("\n⚠ Nenhum empréstimo encontrado!")
            return

        # Se filtro é "atrasados", filtra em Python os que passaram do prazo
        if opcao == "4":
            emprestimos = [
                e
                for e in emprestimos
                if calcular_dias_atraso(e["data_devolucao_prevista"]) > 0
            ]
            if not emprestimos:
                print("\n✓ Nenhum empréstimo atrasado! 🎉")
                return

        print(f"\n{'=' * 90}")
        print(f"📋 {titulo_relatorio} (Total: {len(emprestimos)})")
        print(f"{'=' * 90}")

        # Monta o relatório com dados relacionados
        for emp in emprestimos:
            membro_res = (
                supabase.table(TABELA_MEMBROS)
                .select("nome, tipo")
                .eq("id", emp["membro_id"])
                .execute()
            )
            livro_res = (
                supabase.table(TABELA_LIVROS)
                .select("titulo, autor")
                .eq("id", emp["livro_id"])
                .execute()
            )

            nome_membro = membro_res.data[0]["nome"] if membro_res.data else "N/A"
            tipo_membro = membro_res.data[0]["tipo"] if membro_res.data else "N/A"
            titulo_livro = livro_res.data[0]["titulo"] if livro_res.data else "N/A"
            autor_livro = livro_res.data[0]["autor"] if livro_res.data else "N/A"

            print(f"\n  Empréstimo #{emp['id']}")
            print(f"  📖 Livro: {titulo_livro} ({autor_livro})")
            print(f"  👤 Membro: {nome_membro} ({tipo_membro})")
            print(f"  📅 Empréstimo: {formatar_data(emp['data_emprestimo'])}")
            print(
                f"  📅 Devolução prevista: {formatar_data(emp['data_devolucao_prevista'])}"
            )

            if emp["data_devolucao_real"]:
                print(
                    f"  📅 Devolução real: {formatar_data(emp['data_devolucao_real'])}"
                )

            # Mostra status com contexto
            if emp["status"] == "Ativo":
                dias_atraso = calcular_dias_atraso(emp["data_devolucao_prevista"])
                if dias_atraso > 0:
                    multa_estimada = dias_atraso * MULTA_POR_DIA
                    print(
                        f"  ⚠ STATUS: ATRASADO ({dias_atraso} dias) - Multa estimada: R$ {multa_estimada:.2f}"
                    )
                else:
                    data_prev = datetime.strptime(
                        str(emp["data_devolucao_prevista"]), "%Y-%m-%d"
                    ).date()
                    dias_restantes = (data_prev - date.today()).days
                    print(f"  ✓ STATUS: Ativo ({dias_restantes} dias restantes)")
            else:
                if emp["multa"] and float(emp["multa"]) > 0:
                    print(
                        f"  ✓ STATUS: Devolvido | Multa: R$ {float(emp['multa']):.2f}"
                    )
                else:
                    print(f"  ✓ STATUS: Devolvido (sem multa)")

            print(f"  {'─' * 50}")

    except Exception as e:
        print(f"✗ Erro ao gerar relatório: {e}")


def estatisticas_biblioteca():
    """Calcula e exibe estatísticas completas da biblioteca"""
    try:
        # Busca todos os dados necessários
        livros_res = supabase.table(TABELA_LIVROS).select("*").execute()
        membros_res = supabase.table(TABELA_MEMBROS).select("*").execute()
        emp_res = supabase.table(TABELA_EMPRESTIMOS).select("*").execute()

        livros = livros_res.data
        membros = membros_res.data
        emprestimos = emp_res.data

        print("\n" + "=" * 70)
        print("📊 ESTATÍSTICAS DA BIBLIOTECA")
        print("=" * 70)

        # ---- Estatísticas de Livros ----
        print("\n📚 ACERVO")
        print(f"  Total de títulos: {len(livros)}")
        if livros:
            total_copias = sum(l["quantidade_total"] for l in livros)
            total_disponivel = sum(l["quantidade_disponivel"] for l in livros)
            total_emprestado = total_copias - total_disponivel
            print(f"  Total de cópias: {total_copias}")
            print(f"  Cópias disponíveis: {total_disponivel}")
            print(f"  Cópias emprestadas: {total_emprestado}")

            # Contagem de livros por gênero usando dict comprehension
            generos = {}
            for livro in livros:
                genero = livro["genero"]
                generos[genero] = generos.get(genero, 0) + 1

            print("\n  Livros por gênero:")
            # Ordena gêneros por quantidade (decrescente) usando sorted() com key
            for genero, qtd in sorted(
                generos.items(), key=lambda x: x[1], reverse=True
            ):
                barra = "█" * qtd  # Gráfico de barras simples
                print(f"    {genero:<20} {barra} ({qtd})")

        # ---- Estatísticas de Membros ----
        print(f"\n👥 MEMBROS")
        print(f"  Total de membros: {len(membros)}")
        if membros:
            ativos = sum(1 for m in membros if m["ativo"])
            inativos = len(membros) - ativos
            estudantes = sum(1 for m in membros if m["tipo"] == "Estudante")
            professores = sum(1 for m in membros if m["tipo"] == "Professor")

            print(f"  Ativos: {ativos} | Inativos: {inativos}")
            print(f"  Estudantes: {estudantes} | Professores: {professores}")

        # ---- Estatísticas de Empréstimos ----
        print(f"\n📤 EMPRÉSTIMOS")
        print(f"  Total de empréstimos: {len(emprestimos)}")
        if emprestimos:
            ativos = [e for e in emprestimos if e["status"] == "Ativo"]
            devolvidos = [e for e in emprestimos if e["status"] == "Devolvido"]
            atrasados = [
                e
                for e in ativos
                if calcular_dias_atraso(e["data_devolucao_prevista"]) > 0
            ]

            print(f"  Ativos: {len(ativos)}")
            print(f"  Devolvidos: {len(devolvidos)}")
            print(f"  Atrasados: {len(atrasados)}")

            # Calcula total de multas
            total_multas = sum(float(e.get("multa", 0) or 0) for e in emprestimos)
            if total_multas > 0:
                print(f"\n  💰 Total em multas cobradas: R$ {total_multas:.2f}")

            # Livros mais emprestados (ranking)
            if emprestimos:
                contagem_livros = {}
                for emp in emprestimos:
                    lid = emp["livro_id"]
                    contagem_livros[lid] = contagem_livros.get(lid, 0) + 1

                print("\n  🏆 TOP 5 LIVROS MAIS EMPRESTADOS:")
                # sorted() retorna uma nova lista ordenada
                ranking = sorted(
                    contagem_livros.items(), key=lambda x: x[1], reverse=True
                )[:5]

                for posicao, (lid, qtd) in enumerate(ranking, 1):
                    livro_info = (
                        supabase.table(TABELA_LIVROS)
                        .select("titulo")
                        .eq("id", lid)
                        .execute()
                    )
                    titulo = livro_info.data[0]["titulo"] if livro_info.data else "N/A"
                    medalha = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][posicao - 1]
                    print(f"    {medalha} {titulo} — {qtd} empréstimo(s)")

        print("\n" + "=" * 70)

    except Exception as e:
        print(f"✗ Erro ao calcular estatísticas: {e}")


# ========== MENU PRINCIPAL ==========
def menu_principal():
    """Menu interativo do sistema de biblioteca"""

    while True:
        print("\n" + "=" * 70)
        print("📚 BIBLIOTECA - MENU PRINCIPAL")
        print("=" * 70)
        print("  1. 📖 Cadastrar Livro")
        print("  2. 👤 Cadastrar Membro")
        print("  3. 📤 Realizar Empréstimo")
        print("  4. 📥 Devolver Livro")
        print("  5. 📚 Listar Livros")
        print("  6. 👥 Listar Membros")
        print("  7. 🔍 Buscar Livro")
        print("  8. 📋 Relatório de Empréstimos")
        print("  9. 📊 Estatísticas da Biblioteca")
        print("  0. 🚪 Sair")
        print("=" * 70)

        opcao = input("\nEscolha uma opção: ").strip()

        # Dicionário de funções — alternativa ao if/elif extenso
        # Demonstra que funções são "objetos de primeira classe" em Python
        acoes = {
            "1": cadastrar_livro,
            "2": cadastrar_membro,
            "3": realizar_emprestimo,
            "4": devolver_livro,
            "5": listar_livros,
            "6": listar_membros,
            "7": buscar_livro,
            "8": relatorio_emprestimos,
            "9": estatisticas_biblioteca,
        }

        if opcao == "0":
            print("\n✓ Encerrando sistema... Até logo! 📚")
            break
        elif opcao in acoes:
            acoes[opcao]()  # Chama a função correspondente
        else:
            print("\n✗ Opção inválida! Tente novamente.")


# Executa o sistema
if __name__ == "__main__":
    menu_principal()
