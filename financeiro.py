# ========== SISTEMA DE CONTROLE FINANCEIRO PESSOAL ==========
# Sistema completo de finanças com receitas, despesas, relatórios e gráficos
# Conceitos: datetime, dicionários, formatação, cálculos financeiros, gráficos ASCII

import os
from datetime import datetime, date
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

# Nome da tabela no Supabase
TABELA_TRANSACOES = "transacoes"

# Categorias disponíveis organizadas por tipo
CATEGORIAS_DESPESA = [
    "Alimentação",
    "Transporte",
    "Moradia",
    "Saúde",
    "Educação",
    "Lazer",
    "Vestuário",
    "Contas (água, luz, internet)",
    "Assinaturas",
    "Outro (Despesa)",
]

CATEGORIAS_RECEITA = [
    "Salário",
    "Freelance",
    "Investimentos",
    "Vendas",
    "Presente",
    "Outro (Receita)",
]

# Meses do ano para relatórios
MESES = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


# ========== FUNÇÕES UTILITÁRIAS ==========
def formatar_valor(valor):
    """Formata um valor numérico para o formato monetário brasileiro (R$)"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_data(data_str):
    """Converte string de data ISO (YYYY-MM-DD) para formato brasileiro (DD/MM/YYYY)"""
    try:
        if isinstance(data_str, date):
            return data_str.strftime("%d/%m/%Y")
        data_obj = datetime.strptime(str(data_str), "%Y-%m-%d")
        return data_obj.strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return str(data_str) if data_str else "N/A"


def validar_data(data_texto):
    """
    Valida e converte uma data no formato DD/MM/AAAA para YYYY-MM-DD.
    Retorna a data no formato ISO ou None se inválida.
    """
    try:
        data_obj = datetime.strptime(data_texto, "%d/%m/%Y")
        # Não permite datas futuras
        if data_obj.date() > date.today():
            print("✗ Não é possível registrar transações com data futura!")
            return None
        return data_obj.strftime("%Y-%m-%d")
    except ValueError:
        print("✗ Data inválida! Use o formato DD/MM/AAAA (ex: 25/02/2026)")
        return None


def gerar_barra(valor, valor_maximo, largura=30):
    """
    Gera uma barra visual ASCII proporcional ao valor.
    Usa █ para blocos cheios e ░ para o restante.
    """
    if valor_maximo == 0:
        return "░" * largura
    proporcao = valor / valor_maximo
    blocos_cheios = int(proporcao * largura)
    blocos_vazios = largura - blocos_cheios
    return "█" * blocos_cheios + "░" * blocos_vazios


# ========== FUNÇÕES DE TRANSAÇÕES ==========
def adicionar_transacao():
    """Adiciona uma nova transação (receita ou despesa) no banco de dados"""
    print("\n" + "=" * 60)
    print("💰 NOVA TRANSAÇÃO")
    print("=" * 60)

    # Passo 1: Escolher o tipo
    print("\nTipo de transação:")
    print("  1. 📈 Receita (entrada de dinheiro)")
    print("  2. 📉 Despesa (saída de dinheiro)")

    opcao_tipo = input("\nEscolha (1 ou 2): ").strip()

    if opcao_tipo == "1":
        tipo = "Receita"
        categorias = CATEGORIAS_RECEITA
        emoji = "📈"
    elif opcao_tipo == "2":
        tipo = "Despesa"
        categorias = CATEGORIAS_DESPESA
        emoji = "📉"
    else:
        print("✗ Opção inválida!")
        return

    # Passo 2: Descrição
    descricao = input(f"\nDescrição da {tipo.lower()}: ").strip()
    if not descricao:
        print("✗ Descrição não pode ser vazia!")
        return

    # Passo 3: Valor
    try:
        valor_texto = input("Valor (R$): ").strip().replace(",", ".")
        valor = float(valor_texto)
        if valor <= 0:
            print("✗ O valor deve ser maior que zero!")
            return
    except ValueError:
        print("✗ Valor inválido! Digite um número (ex: 150.00 ou 150,00)")
        return

    # Passo 4: Categoria
    print(f"\nCategorias de {tipo}:")
    for i, cat in enumerate(categorias, 1):
        print(f"  {i:2d}. {cat}")

    try:
        opcao_cat = int(input("\nEscolha o número da categoria: "))
        if not 1 <= opcao_cat <= len(categorias):
            print("✗ Opção de categoria inválida!")
            return
        categoria = categorias[opcao_cat - 1]
    except ValueError:
        print("✗ Digite um número válido!")
        return

    # Passo 5: Data
    print(
        f"\nData da transação (pressione ENTER para usar hoje - {formatar_data(date.today())}):"
    )
    data_texto = input("Data (DD/MM/AAAA): ").strip()

    if data_texto == "":
        data_iso = date.today().isoformat()
    else:
        data_iso = validar_data(data_texto)
        if data_iso is None:
            return

    # Passo 6: Salvar no banco
    try:
        dados = {
            "tipo": tipo,
            "descricao": descricao,
            "valor": valor,
            "categoria": categoria,
            "data": data_iso,
        }

        supabase.table(TABELA_TRANSACOES).insert(dados).execute()

        print(f"\n{'=' * 60}")
        print(f"✓ {emoji} {tipo.upper()} REGISTRADA COM SUCESSO!")
        print(f"{'=' * 60}")
        print(f"  Descrição: {descricao}")
        print(f"  Valor: {formatar_valor(valor)}")
        print(f"  Categoria: {categoria}")
        print(f"  Data: {formatar_data(data_iso)}")

    except Exception as e:
        print(f"✗ Erro ao registrar transação: {e}")


def listar_transacoes():
    """Lista as transações mais recentes com filtro por tipo"""
    print("\n" + "=" * 60)
    print("📋 LISTAR TRANSAÇÕES")
    print("=" * 60)
    print("1. Todas as transações")
    print("2. Apenas receitas")
    print("3. Apenas despesas")

    opcao = input("\nEscolha: ").strip()

    try:
        query = supabase.table(TABELA_TRANSACOES).select("*")

        if opcao == "2":
            query = query.eq("tipo", "Receita")
            titulo = "RECEITAS"
        elif opcao == "3":
            query = query.eq("tipo", "Despesa")
            titulo = "DESPESAS"
        elif opcao == "1":
            titulo = "TODAS AS TRANSAÇÕES"
        else:
            print("✗ Opção inválida!")
            return

        resultado = query.order("data", desc=True).limit(50).execute()
        transacoes = resultado.data

        if not transacoes:
            print("\n⚠ Nenhuma transação encontrada!")
            return

        print(f"\n{'=' * 90}")
        print(f"📋 {titulo} (Exibindo: {len(transacoes)})")
        print(f"{'=' * 90}")

        # Cabeçalho da tabela
        print(
            f"\n{'Data':<12} {'Tipo':<10} {'Categoria':<25} {'Descrição':<25} {'Valor':>12}"
        )
        print("-" * 90)

        total_receitas = 0
        total_despesas = 0

        for t in transacoes:
            emoji = "📈" if t["tipo"] == "Receita" else "📉"

            # Trunca descrição e categoria se necessário
            desc = (
                t["descricao"][:23] + ".."
                if len(t["descricao"]) > 25
                else t["descricao"]
            )
            cat = (
                t["categoria"][:23] + ".."
                if len(t["categoria"]) > 25
                else t["categoria"]
            )

            valor_formatado = formatar_valor(t["valor"])

            print(
                f"{formatar_data(t['data']):<12} {emoji} {t['tipo']:<7} {cat:<25} {desc:<25} {valor_formatado:>12}"
            )

            if t["tipo"] == "Receita":
                total_receitas += t["valor"]
            else:
                total_despesas += t["valor"]

        print("-" * 90)
        print(f"  📈 Total Receitas: {formatar_valor(total_receitas)}")
        print(f"  📉 Total Despesas: {formatar_valor(total_despesas)}")
        saldo = total_receitas - total_despesas
        emoji_saldo = "✅" if saldo >= 0 else "🔴"
        print(f"  {emoji_saldo} Saldo: {formatar_valor(saldo)}")

    except Exception as e:
        print(f"✗ Erro ao listar transações: {e}")


def buscar_transacao():
    """Busca transações por descrição ou categoria"""
    print("\n" + "=" * 60)
    print("🔍 BUSCAR TRANSAÇÃO")
    print("=" * 60)
    print("1. Buscar por descrição")
    print("2. Buscar por categoria")

    opcao = input("\nEscolha: ").strip()
    termo = input("Digite o termo de busca: ").strip()

    if not termo:
        print("✗ Termo de busca não pode ser vazio!")
        return

    try:
        campo_busca = {"1": "descricao", "2": "categoria"}

        if opcao not in campo_busca:
            print("✗ Opção inválida!")
            return

        campo = campo_busca[opcao]

        resultado = (
            supabase.table(TABELA_TRANSACOES)
            .select("*")
            .ilike(campo, f"%{termo}%")
            .order("data", desc=True)
            .execute()
        )
        transacoes = resultado.data

        if not transacoes:
            print(f"✗ Nenhuma transação encontrada com '{termo}'")
            return

        print(f"\n✓ Encontradas: {len(transacoes)} transação(ões)")
        print("-" * 60)

        total = 0
        for t in transacoes:
            emoji = "📈" if t["tipo"] == "Receita" else "📉"
            print(f"\n  {emoji} {t['descricao']} (ID: {t['id']})")
            print(f"     Valor: {formatar_valor(t['valor'])}")
            print(f"     Categoria: {t['categoria']}")
            print(f"     Data: {formatar_data(t['data'])}")

            if t["tipo"] == "Receita":
                total += t["valor"]
            else:
                total -= t["valor"]

        print("-" * 60)
        print(f"  Impacto total das transações encontradas: {formatar_valor(total)}")

    except Exception as e:
        print(f"✗ Erro ao buscar transação: {e}")


def editar_transacao():
    """Edita uma transação existente"""
    print("\n" + "=" * 60)
    print("✏️  EDITAR TRANSAÇÃO")
    print("=" * 60)

    try:
        id_transacao = int(input("Digite o ID da transação: "))
    except ValueError:
        print("✗ Digite um ID válido!")
        return

    try:
        resultado = (
            supabase.table(TABELA_TRANSACOES)
            .select("*")
            .eq("id", id_transacao)
            .execute()
        )

        if not resultado.data:
            print("✗ Transação não encontrada!")
            return

        t = resultado.data[0]

        emoji = "📈" if t["tipo"] == "Receita" else "📉"
        print(f"\n  {emoji} Transação atual:")
        print(f"     Descrição: {t['descricao']}")
        print(f"     Valor: {formatar_valor(t['valor'])}")
        print(f"     Categoria: {t['categoria']}")
        print(f"     Data: {formatar_data(t['data'])}")

        print("\n  O que deseja editar? (pressione ENTER para manter)")

        # Editar descrição
        nova_descricao = input(f"  Nova descrição [{t['descricao']}]: ").strip()
        if not nova_descricao:
            nova_descricao = t["descricao"]

        # Editar valor
        novo_valor_texto = input(
            f"  Novo valor [{formatar_valor(t['valor'])}]: "
        ).strip()
        if novo_valor_texto:
            try:
                novo_valor = float(novo_valor_texto.replace(",", "."))
                if novo_valor <= 0:
                    print("✗ Valor deve ser maior que zero!")
                    return
            except ValueError:
                print("✗ Valor inválido!")
                return
        else:
            novo_valor = t["valor"]

        # Editar categoria
        categorias = (
            CATEGORIAS_RECEITA if t["tipo"] == "Receita" else CATEGORIAS_DESPESA
        )
        print(f"\n  Categorias disponíveis:")
        for i, cat in enumerate(categorias, 1):
            marcador = " ◀" if cat == t["categoria"] else ""
            print(f"    {i:2d}. {cat}{marcador}")

        opcao_cat = input(f"  Nova categoria (número) [{t['categoria']}]: ").strip()
        if opcao_cat:
            try:
                idx = int(opcao_cat)
                if 1 <= idx <= len(categorias):
                    nova_categoria = categorias[idx - 1]
                else:
                    print("✗ Opção inválida!")
                    return
            except ValueError:
                print("✗ Digite um número válido!")
                return
        else:
            nova_categoria = t["categoria"]

        # Editar data
        nova_data_texto = input(
            f"  Nova data (DD/MM/AAAA) [{formatar_data(t['data'])}]: "
        ).strip()
        if nova_data_texto:
            nova_data = validar_data(nova_data_texto)
            if nova_data is None:
                return
        else:
            nova_data = t["data"]

        # Salvar alterações
        dados_atualizacao = {
            "descricao": nova_descricao,
            "valor": novo_valor,
            "categoria": nova_categoria,
            "data": nova_data,
        }

        supabase.table(TABELA_TRANSACOES).update(dados_atualizacao).eq(
            "id", id_transacao
        ).execute()

        print(f"\n{'=' * 60}")
        print("✓ TRANSAÇÃO ATUALIZADA COM SUCESSO!")
        print(f"{'=' * 60}")
        print(f"  Descrição: {nova_descricao}")
        print(f"  Valor: {formatar_valor(novo_valor)}")
        print(f"  Categoria: {nova_categoria}")
        print(f"  Data: {formatar_data(nova_data)}")

    except Exception as e:
        print(f"✗ Erro ao editar transação: {e}")


def excluir_transacao():
    """Exclui uma transação do banco de dados"""
    print("\n" + "=" * 60)
    print("🗑️  EXCLUIR TRANSAÇÃO")
    print("=" * 60)

    try:
        id_transacao = int(input("Digite o ID da transação: "))
    except ValueError:
        print("✗ Digite um ID válido!")
        return

    try:
        resultado = (
            supabase.table(TABELA_TRANSACOES)
            .select("*")
            .eq("id", id_transacao)
            .execute()
        )

        if not resultado.data:
            print("✗ Transação não encontrada!")
            return

        t = resultado.data[0]

        emoji = "📈" if t["tipo"] == "Receita" else "📉"
        print(f"\n  {emoji} Transação a ser excluída:")
        print(f"     Descrição: {t['descricao']}")
        print(f"     Valor: {formatar_valor(t['valor'])}")
        print(f"     Data: {formatar_data(t['data'])}")

        confirmacao = input("\n  Tem certeza? (s/n): ").strip().lower()
        if confirmacao != "s":
            print("  Operação cancelada.")
            return

        supabase.table(TABELA_TRANSACOES).delete().eq("id", id_transacao).execute()
        print("\n✓ Transação excluída com sucesso!")

    except Exception as e:
        print(f"✗ Erro ao excluir transação: {e}")


# ========== RELATÓRIOS ==========
def relatorio_mensal():
    """Gera relatório detalhado de um mês específico com gráficos ASCII"""
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO MENSAL")
    print("=" * 60)

    # Escolher mês e ano
    print("\nMeses:")
    for i, mes in enumerate(MESES, 1):
        print(f"  {i:2d}. {mes}")

    try:
        mes_num = int(input("\nEscolha o mês: "))
        if not 1 <= mes_num <= 12:
            print("✗ Mês inválido!")
            return

        ano = int(
            input(f"Ano (padrão: {date.today().year}): ") or str(date.today().year)
        )
        if not 2020 <= ano <= 2030:
            print("✗ Ano inválido!")
            return
    except ValueError:
        print("✗ Digite valores numéricos válidos!")
        return

    # Calcula primeiro e último dia do mês
    primeiro_dia = f"{ano}-{mes_num:02d}-01"
    if mes_num == 12:
        ultimo_dia = f"{ano + 1}-01-01"
    else:
        ultimo_dia = f"{ano}-{mes_num + 1:02d}-01"

    try:
        # Busca transações do mês
        resultado = (
            supabase.table(TABELA_TRANSACOES)
            .select("*")
            .gte("data", primeiro_dia)
            .lt("data", ultimo_dia)
            .order("data")
            .execute()
        )
        transacoes = resultado.data

        nome_mes = MESES[mes_num - 1]

        print(f"\n{'=' * 70}")
        print(f"📊 RELATÓRIO FINANCEIRO — {nome_mes.upper()} / {ano}")
        print(f"{'=' * 70}")

        if not transacoes:
            print("\n⚠ Nenhuma transação encontrada neste mês!")
            return

        # Separa receitas e despesas
        receitas = [t for t in transacoes if t["tipo"] == "Receita"]
        despesas = [t for t in transacoes if t["tipo"] == "Despesa"]

        total_receitas = sum(t["valor"] for t in receitas)
        total_despesas = sum(t["valor"] for t in despesas)
        saldo = total_receitas - total_despesas

        # ---- Resumo Geral ----
        print("\n  ┌────────────────────────────────────────────────────┐")
        print("  │               RESUMO DO MÊS                       │")
        print("  ├────────────────────────────────────────────────────┤")
        print(f"  │  📈 Receitas:  {formatar_valor(total_receitas):>20}           │")
        print(f"  │  📉 Despesas:  {formatar_valor(total_despesas):>20}           │")
        print("  ├────────────────────────────────────────────────────┤")

        if saldo >= 0:
            print(f"  │  ✅ Saldo:     {formatar_valor(saldo):>20}           │")
        else:
            print(f"  │  🔴 Saldo:     {formatar_valor(saldo):>20}           │")

        print("  └────────────────────────────────────────────────────┘")

        # ---- Proporção Receitas vs Despesas (barra visual) ----
        total_geral = total_receitas + total_despesas
        if total_geral > 0:
            pct_receita = (total_receitas / total_geral) * 100
            pct_despesa = (total_despesas / total_geral) * 100

            print("\n  Proporção Receitas vs Despesas:")
            print(
                f"  📈 Receitas [{pct_receita:5.1f}%] {gerar_barra(total_receitas, total_geral, 40)}"
            )
            print(
                f"  📉 Despesas [{pct_despesa:5.1f}%] {gerar_barra(total_despesas, total_geral, 40)}"
            )

        # ---- Despesas por Categoria (gráfico de barras) ----
        if despesas:
            print(f"\n  {'─' * 60}")
            print("  📉 DESPESAS POR CATEGORIA")
            print(f"  {'─' * 60}")

            # Agrupa despesas por categoria
            gastos_por_categoria = {}
            for d in despesas:
                cat = d["categoria"]
                gastos_por_categoria[cat] = (
                    gastos_por_categoria.get(cat, 0) + d["valor"]
                )

            # Ordena por valor (maior para menor)
            categorias_ordenadas = sorted(
                gastos_por_categoria.items(), key=lambda x: x[1], reverse=True
            )

            maior_valor = categorias_ordenadas[0][1] if categorias_ordenadas else 0

            for cat, valor in categorias_ordenadas:
                pct = (valor / total_despesas) * 100 if total_despesas > 0 else 0
                barra = gerar_barra(valor, maior_valor, 25)
                print(f"  {cat:<28} {barra} {formatar_valor(valor):>12} ({pct:5.1f}%)")

        # ---- Receitas por Categoria ----
        if receitas:
            print(f"\n  {'─' * 60}")
            print("  📈 RECEITAS POR CATEGORIA")
            print(f"  {'─' * 60}")

            ganhos_por_categoria = {}
            for r in receitas:
                cat = r["categoria"]
                ganhos_por_categoria[cat] = (
                    ganhos_por_categoria.get(cat, 0) + r["valor"]
                )

            categorias_ordenadas = sorted(
                ganhos_por_categoria.items(), key=lambda x: x[1], reverse=True
            )

            maior_valor = categorias_ordenadas[0][1] if categorias_ordenadas else 0

            for cat, valor in categorias_ordenadas:
                pct = (valor / total_receitas) * 100 if total_receitas > 0 else 0
                barra = gerar_barra(valor, maior_valor, 25)
                print(f"  {cat:<28} {barra} {formatar_valor(valor):>12} ({pct:5.1f}%)")

        # ---- Lista detalhada ----
        print(f"\n  {'─' * 60}")
        print(f"  📋 TRANSAÇÕES DO MÊS ({len(transacoes)} registros)")
        print(f"  {'─' * 60}")

        for t in transacoes:
            emoji = "📈" if t["tipo"] == "Receita" else "📉"
            print(
                f"  {formatar_data(t['data'])} {emoji} {t['descricao']:<30} {formatar_valor(t['valor']):>12}"
            )

    except Exception as e:
        print(f"✗ Erro ao gerar relatório: {e}")


def estatisticas_financeiras():
    """Calcula e exibe estatísticas completas das finanças"""
    try:
        resultado = (
            supabase.table(TABELA_TRANSACOES).select("*").order("data").execute()
        )
        transacoes = resultado.data

        if not transacoes:
            print("\n⚠ Nenhuma transação cadastrada!")
            return

        print(f"\n{'=' * 70}")
        print("📊 ESTATÍSTICAS FINANCEIRAS")
        print(f"{'=' * 70}")

        # Separa por tipo
        receitas = [t for t in transacoes if t["tipo"] == "Receita"]
        despesas = [t for t in transacoes if t["tipo"] == "Despesa"]

        total_receitas = sum(t["valor"] for t in receitas)
        total_despesas = sum(t["valor"] for t in despesas)
        saldo_total = total_receitas - total_despesas

        # ---- Visão Geral ----
        print("\n  💰 VISÃO GERAL")
        print(f"  Total de transações: {len(transacoes)}")
        print(
            f"  Receitas: {len(receitas)} transações = {formatar_valor(total_receitas)}"
        )
        print(
            f"  Despesas: {len(despesas)} transações = {formatar_valor(total_despesas)}"
        )

        emoji_saldo = "✅" if saldo_total >= 0 else "🔴"
        print(f"  {emoji_saldo} Saldo geral: {formatar_valor(saldo_total)}")

        # ---- Médias ----
        print(f"\n  📏 MÉDIAS")
        if receitas:
            media_receita = total_receitas / len(receitas)
            maior_receita = max(receitas, key=lambda x: x["valor"])
            print(f"  Média por receita: {formatar_valor(media_receita)}")
            print(
                f"  Maior receita: {formatar_valor(maior_receita['valor'])} ({maior_receita['descricao']})"
            )

        if despesas:
            media_despesa = total_despesas / len(despesas)
            maior_despesa = max(despesas, key=lambda x: x["valor"])
            menor_despesa = min(despesas, key=lambda x: x["valor"])
            print(f"  Média por despesa: {formatar_valor(media_despesa)}")
            print(
                f"  Maior despesa: {formatar_valor(maior_despesa['valor'])} ({maior_despesa['descricao']})"
            )
            print(
                f"  Menor despesa: {formatar_valor(menor_despesa['valor'])} ({menor_despesa['descricao']})"
            )

        # ---- Top 5 maiores despesas ----
        if despesas:
            print(f"\n  🏆 TOP 5 MAIORES DESPESAS")
            despesas_ordenadas = sorted(
                despesas, key=lambda x: x["valor"], reverse=True
            )
            for i, d in enumerate(despesas_ordenadas[:5], 1):
                print(
                    f"  {i}. {formatar_valor(d['valor']):>12} — {d['descricao']} ({formatar_data(d['data'])})"
                )

        # ---- Gastos por Categoria (todas as transações) ----
        if despesas:
            print(f"\n  📂 DESPESAS POR CATEGORIA (GERAL)")
            print(f"  {'─' * 55}")

            gastos_por_categoria = {}
            for d in despesas:
                cat = d["categoria"]
                gastos_por_categoria[cat] = (
                    gastos_por_categoria.get(cat, 0) + d["valor"]
                )

            categorias_ordenadas = sorted(
                gastos_por_categoria.items(), key=lambda x: x[1], reverse=True
            )

            maior_valor = categorias_ordenadas[0][1] if categorias_ordenadas else 0

            for cat, valor in categorias_ordenadas:
                pct = (valor / total_despesas) * 100 if total_despesas > 0 else 0
                barra = gerar_barra(valor, maior_valor, 20)
                print(f"  {cat:<28} {barra} {formatar_valor(valor):>12} ({pct:5.1f}%)")

        # ---- Evolução mensal (gráfico de barras) ----
        print(f"\n  📈 EVOLUÇÃO MENSAL")
        print(f"  {'─' * 55}")

        # Agrupa transações por mês
        meses_dados = {}
        for t in transacoes:
            chave_mes = t["data"][:7]  # Pega YYYY-MM
            if chave_mes not in meses_dados:
                meses_dados[chave_mes] = {"receitas": 0, "despesas": 0}

            if t["tipo"] == "Receita":
                meses_dados[chave_mes]["receitas"] += t["valor"]
            else:
                meses_dados[chave_mes]["despesas"] += t["valor"]

        # Encontra o maior valor para escala das barras
        todos_valores = []
        for dados in meses_dados.values():
            todos_valores.append(dados["receitas"])
            todos_valores.append(dados["despesas"])
        maior_valor_mensal = max(todos_valores) if todos_valores else 0

        # Exibe mês a mês em ordem cronológica
        for chave_mes in sorted(meses_dados.keys()):
            dados = meses_dados[chave_mes]
            ano_mes = chave_mes.split("-")
            nome_mes_label = f"{MESES[int(ano_mes[1]) - 1][:3]}/{ano_mes[0]}"

            saldo_mes = dados["receitas"] - dados["despesas"]
            emoji_mes = "✅" if saldo_mes >= 0 else "🔴"

            barra_rec = gerar_barra(dados["receitas"], maior_valor_mensal, 15)
            barra_desp = gerar_barra(dados["despesas"], maior_valor_mensal, 15)

            print(
                f"  {nome_mes_label:<10} 📈 {barra_rec} {formatar_valor(dados['receitas']):>12}"
            )
            print(f"  {'':10} 📉 {barra_desp} {formatar_valor(dados['despesas']):>12}")
            print(f"  {'':10} {emoji_mes}  Saldo: {formatar_valor(saldo_mes)}")
            print()

    except Exception as e:
        print(f"✗ Erro ao calcular estatísticas: {e}")


# ========== MENU PRINCIPAL ==========
def menu_principal():
    """Menu interativo do sistema financeiro"""
    while True:
        print("\n" + "=" * 60)
        print("💰 CONTROLE FINANCEIRO PESSOAL")
        print("=" * 60)
        print("  1. 💰 Nova Transação (Receita/Despesa)")
        print("  2. 📋 Listar Transações")
        print("  3. 🔍 Buscar Transação")
        print("  4. ✏️  Editar Transação")
        print("  5. 🗑️  Excluir Transação")
        print("  6. 📊 Relatório Mensal")
        print("  7. 📈 Estatísticas Financeiras")
        print("  0. 🚪 Sair")
        print("=" * 60)

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            adicionar_transacao()
        elif opcao == "2":
            listar_transacoes()
        elif opcao == "3":
            buscar_transacao()
        elif opcao == "4":
            editar_transacao()
        elif opcao == "5":
            excluir_transacao()
        elif opcao == "6":
            relatorio_mensal()
        elif opcao == "7":
            estatisticas_financeiras()
        elif opcao == "0":
            print("\n✓ Encerrando sistema financeiro... Até logo! 👋")
            break
        else:
            print("\n✗ Opção inválida! Tente novamente.")


# Executa o sistema
if __name__ == "__main__":
    menu_principal()
