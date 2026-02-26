# ========== DASHBOARD FINANCEIRO — STREAMLIT ==========
# Dashboard visual conectado ao Supabase (mesma tabela do financeiro.py)
# Conceitos: Streamlit, Plotly, Pandas, visualização de dados, filtros interativos

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from dotenv import load_dotenv
from supabase import create_client

# ========== CONFIGURAÇÃO DA PÁGINA ==========
st.set_page_config(
    page_title="💰 Dashboard Financeiro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ========== CSS PERSONALIZADO ==========
st.markdown(
    """
    <style>
    /* Importa fonte moderna do Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Aplica fonte em toda a página */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Estilo do título principal */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* Cards de KPI */
    .kpi-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.3rem 0;
    }
    .kpi-receita { color: #48bb78; }
    .kpi-despesa { color: #fc8181; }
    .kpi-saldo-positivo { color: #4fd1c5; }
    .kpi-saldo-negativo { color: #fc8181; }
    .kpi-total { color: #a78bfa; }

    /* Container de seção */
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #e2e8f0;
        margin: 1.5rem 0 0.8rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.4);
    }

    /* Sidebar mais bonita */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #a78bfa;
    }

    /* Divider customizado */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        margin: 1.5rem 0;
        border: none;
    }

    /* Esconde o header padrão do Streamlit */
    header[data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0);
    }

    /* Texto dos radio buttons, labels e widgets na sidebar */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        color: #e2e8f0 !important;
    }

    /* Texto dentro dos radio buttons (as opções) */
    [data-testid="stSidebar"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        color: #cbd5e0 !important;
        font-weight: 500;
    }

    /* Texto dentro de selectbox e multiselect */
    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #e2e8f0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ========== CONEXÃO COM SUPABASE ==========
@st.cache_resource
def conectar_supabase():
    """Conecta ao Supabase usando variáveis de ambiente (com cache)"""
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        st.error("⚠ Configure as credenciais do Supabase no arquivo .env!")
        st.stop()

    return create_client(url, key)


supabase = conectar_supabase()
TABELA_TRANSACOES = "transacoes"

# Nomes dos meses em português
MESES_PT = [
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
MESES_ABREV = [
    "Jan",
    "Fev",
    "Mar",
    "Abr",
    "Mai",
    "Jun",
    "Jul",
    "Ago",
    "Set",
    "Out",
    "Nov",
    "Dez",
]


# ========== FUNÇÕES DE DADOS ==========
@st.cache_data(ttl=60)
def carregar_transacoes():
    """Carrega todas as transações do Supabase e retorna como DataFrame"""
    resultado = (
        supabase.table(TABELA_TRANSACOES).select("*").order("data", desc=True).execute()
    )

    if not resultado.data:
        return pd.DataFrame()

    df = pd.DataFrame(resultado.data)
    df["data"] = pd.to_datetime(df["data"])
    df["mes"] = df["data"].dt.month
    df["ano"] = df["data"].dt.year
    df["mes_nome"] = df["mes"].apply(lambda m: MESES_PT[m - 1])
    df["mes_abrev"] = df["mes"].apply(lambda m: MESES_ABREV[m - 1])
    df["mes_ano"] = df["data"].dt.strftime("%m/%Y")
    return df


def formatar_valor(valor):
    """Formata um valor numérico para o formato monetário brasileiro (R$)"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ========== LAYOUT DOS GRÁFICOS (cores e tema) ==========
CORES = {
    "receita": "#48bb78",
    "despesa": "#fc8181",
    "saldo_positivo": "#4fd1c5",
    "saldo_negativo": "#fc8181",
    "gradiente": ["#667eea", "#764ba2", "#f093fb", "#f5576c", "#4facfe", "#43e97b"],
    "categorias": px.colors.qualitative.Pastel,
}

LAYOUT_PADRAO = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#e2e8f0"),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(
        bgcolor="rgba(0,0,0,0.3)",
        bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1,
        font=dict(size=11),
    ),
)


# ========== COMPONENTES VISUAIS ==========
def renderizar_kpis(df_filtrado):
    """Renderiza os cards de KPI (Receitas, Despesas, Saldo, Total)"""
    receitas = df_filtrado[df_filtrado["tipo"] == "Receita"]["valor"].sum()
    despesas = df_filtrado[df_filtrado["tipo"] == "Despesa"]["valor"].sum()
    saldo = receitas - despesas
    total_transacoes = len(df_filtrado)

    classe_saldo = "kpi-saldo-positivo" if saldo >= 0 else "kpi-saldo-negativo"
    emoji_saldo = "📈" if saldo >= 0 else "📉"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">📈 Receitas</div>
                <div class="kpi-value kpi-receita">{formatar_valor(receitas)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">📉 Despesas</div>
                <div class="kpi-value kpi-despesa">{formatar_valor(despesas)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{emoji_saldo} Saldo</div>
                <div class="kpi-value {classe_saldo}">{formatar_valor(saldo)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">📊 Transações</div>
                <div class="kpi-value kpi-total">{total_transacoes}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def grafico_pizza_categorias(df_filtrado, tipo="Despesa"):
    """Gráfico de pizza (donut) com gastos ou receitas por categoria"""
    df_tipo = df_filtrado[df_filtrado["tipo"] == tipo]

    if df_tipo.empty:
        st.info(
            f"Nenhuma {'despesa' if tipo == 'Despesa' else 'receita'} no período selecionado."
        )
        return

    df_agrupado = df_tipo.groupby("categoria")["valor"].sum().reset_index()
    df_agrupado = df_agrupado.sort_values("valor", ascending=False)

    cor_titulo = CORES["despesa"] if tipo == "Despesa" else CORES["receita"]
    emoji = "📉" if tipo == "Despesa" else "📈"

    fig = px.pie(
        df_agrupado,
        values="valor",
        names="categoria",
        hole=0.45,
        color_discrete_sequence=CORES["categorias"],
    )

    fig.update_traces(
        textposition="outside",
        textinfo="label+percent",
        textfont_size=11,
        marker=dict(line=dict(color="#1a1a2e", width=2)),
        hovertemplate="<b>%{label}</b><br>Valor: R$ %{value:,.2f}<br>Percentual: %{percent}<extra></extra>",
    )

    fig.update_layout(
        **LAYOUT_PADRAO,
        title=dict(
            text=f"{emoji} {tipo}s por Categoria",
            font=dict(size=16, color=cor_titulo),
        ),
        showlegend=True,
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)


def grafico_barras_mensal(df_filtrado):
    """Gráfico de barras comparando receitas vs despesas por mês"""
    if df_filtrado.empty:
        st.info("Nenhum dado para exibir.")
        return

    # Agrupa por mês/ano e tipo
    df_filtrado = df_filtrado.copy()
    df_filtrado["periodo"] = df_filtrado["data"].dt.to_period("M").astype(str)

    df_agrupado = df_filtrado.groupby(["periodo", "tipo"])["valor"].sum().reset_index()

    # Ordena cronologicamente
    df_agrupado = df_agrupado.sort_values("periodo")

    # Formata labels dos meses
    def formatar_periodo(p):
        partes = p.split("-")
        mes_idx = int(partes[1]) - 1
        return f"{MESES_ABREV[mes_idx]}/{partes[0][-2:]}"

    df_agrupado["periodo_label"] = df_agrupado["periodo"].apply(formatar_periodo)

    cor_map = {"Receita": CORES["receita"], "Despesa": CORES["despesa"]}

    fig = px.bar(
        df_agrupado,
        x="periodo_label",
        y="valor",
        color="tipo",
        barmode="group",
        color_discrete_map=cor_map,
        labels={"periodo_label": "Período", "valor": "Valor (R$)", "tipo": "Tipo"},
    )

    fig.update_layout(
        **LAYOUT_PADRAO,
        title=dict(
            text="📊 Receitas vs Despesas por Mês", font=dict(size=16, color="#a78bfa")
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=""),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Valor (R$)"),
        height=400,
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{data.name}: R$ %{y:,.2f}<extra></extra>",
        marker_line_color="#1a1a2e",
        marker_line_width=1,
    )

    st.plotly_chart(fig, use_container_width=True)


def grafico_evolucao_saldo(df_filtrado):
    """Gráfico de linha mostrando a evolução do saldo acumulado"""
    if df_filtrado.empty:
        st.info("Nenhum dado para exibir.")
        return

    df_sorted = df_filtrado.sort_values("data").copy()

    # Calcula valor com sinal (receita positiva, despesa negativa)
    df_sorted["valor_sinal"] = df_sorted.apply(
        lambda row: row["valor"] if row["tipo"] == "Receita" else -row["valor"],
        axis=1,
    )

    # Agrupa por dia e calcula saldo acumulado
    df_diario = df_sorted.groupby("data")["valor_sinal"].sum().reset_index()
    df_diario["saldo_acumulado"] = df_diario["valor_sinal"].cumsum()

    # Define cor baseada no saldo
    cor_linha = (
        CORES["saldo_positivo"]
        if df_diario["saldo_acumulado"].iloc[-1] >= 0
        else CORES["saldo_negativo"]
    )

    fig = go.Figure()

    # Área preenchida abaixo da linha
    fig.add_trace(
        go.Scatter(
            x=df_diario["data"],
            y=df_diario["saldo_acumulado"],
            mode="lines",
            fill="tozeroy",
            line=dict(color=cor_linha, width=2.5),
            fillcolor=f"rgba({int(cor_linha[1:3], 16)}, {int(cor_linha[3:5], 16)}, {int(cor_linha[5:7], 16)}, 0.15)",
            name="Saldo Acumulado",
            hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Saldo: R$ %{y:,.2f}<extra></extra>",
        )
    )

    # Linha de referência em zero
    fig.add_hline(
        y=0, line_dash="dot", line_color="rgba(255,255,255,0.3)", line_width=1
    )

    fig.update_layout(
        **LAYOUT_PADRAO,
        title=dict(
            text="📈 Evolução do Saldo Acumulado", font=dict(size=16, color="#4fd1c5")
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title=""),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Saldo (R$)"),
        height=350,
        showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)


def grafico_barras_categorias(df_filtrado):
    """Gráfico de barras horizontais com despesas por categoria"""
    df_despesas = df_filtrado[df_filtrado["tipo"] == "Despesa"]

    if df_despesas.empty:
        st.info("Nenhuma despesa no período selecionado.")
        return

    df_agrupado = df_despesas.groupby("categoria")["valor"].sum().reset_index()
    df_agrupado = df_agrupado.sort_values("valor", ascending=True)

    fig = px.bar(
        df_agrupado,
        x="valor",
        y="categoria",
        orientation="h",
        color="valor",
        color_continuous_scale=["#667eea", "#764ba2", "#f5576c"],
    )

    fig.update_layout(
        **LAYOUT_PADRAO,
        title=dict(
            text="📉 Ranking de Despesas por Categoria",
            font=dict(size=16, color="#fc8181"),
        ),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Valor Total (R$)"),
        yaxis=dict(title=""),
        coloraxis_showscale=False,
        height=400,
    )

    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Total: R$ %{x:,.2f}<extra></extra>",
        marker_line_color="#1a1a2e",
        marker_line_width=1,
    )

    st.plotly_chart(fig, use_container_width=True)


def tabela_transacoes(df_filtrado):
    """Exibe tabela interativa com as transações"""
    if df_filtrado.empty:
        st.info("Nenhuma transação no período selecionado.")
        return

    df_tabela = df_filtrado[["data", "tipo", "descricao", "categoria", "valor"]].copy()
    df_tabela["data"] = df_tabela["data"].dt.strftime("%d/%m/%Y")
    df_tabela["valor"] = df_tabela["valor"].apply(formatar_valor)

    df_tabela.columns = [
        "📅 Data",
        "📊 Tipo",
        "📝 Descrição",
        "📂 Categoria",
        "💰 Valor",
    ]

    st.dataframe(
        df_tabela,
        use_container_width=True,
        hide_index=True,
        height=400,
    )


# ========== SIDEBAR E FILTROS ==========
def configurar_sidebar(df):
    """Configura a barra lateral com filtros e retorna o DataFrame filtrado"""
    st.sidebar.markdown("# 💰 Financeiro")
    st.sidebar.markdown("---")

    # Tipo de relatório
    st.sidebar.markdown("### 📋 Período do Relatório")
    tipo_relatorio = st.sidebar.radio(
        "Selecione o período:",
        options=["📅 Mês Isolado", "📆 Ano Isolado", "📊 Todo o Histórico"],
        index=0,
        label_visibility="collapsed",
    )

    df_filtrado = df.copy()

    if tipo_relatorio == "📅 Mês Isolado":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🗓️ Selecione o Mês")

        # Descobre os anos disponíveis
        anos_disponiveis = (
            sorted(df["ano"].unique(), reverse=True)
            if not df.empty
            else [date.today().year]
        )
        ano_selecionado = st.sidebar.selectbox("Ano:", anos_disponiveis)

        mes_selecionado = st.sidebar.selectbox(
            "Mês:",
            range(1, 13),
            format_func=lambda m: MESES_PT[m - 1],
            index=date.today().month - 1,
        )

        df_filtrado = df_filtrado[
            (df_filtrado["ano"] == ano_selecionado)
            & (df_filtrado["mes"] == mes_selecionado)
        ]

        titulo_periodo = f"{MESES_PT[mes_selecionado - 1]} / {ano_selecionado}"

    elif tipo_relatorio == "📆 Ano Isolado":
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📆 Selecione o Ano")

        anos_disponiveis = (
            sorted(df["ano"].unique(), reverse=True)
            if not df.empty
            else [date.today().year]
        )
        ano_selecionado = st.sidebar.selectbox("Ano:", anos_disponiveis)

        df_filtrado = df_filtrado[df_filtrado["ano"] == ano_selecionado]

        titulo_periodo = f"Ano {ano_selecionado}"

    else:
        titulo_periodo = "Todo o Histórico"

    # Filtros adicionais
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Filtros Extras")

    tipo_transacao = st.sidebar.multiselect(
        "Tipo de transação:",
        options=["Receita", "Despesa"],
        default=["Receita", "Despesa"],
    )

    if tipo_transacao:
        df_filtrado = df_filtrado[df_filtrado["tipo"].isin(tipo_transacao)]

    # Filtro por categoria
    if not df_filtrado.empty:
        categorias_disponiveis = sorted(df_filtrado["categoria"].unique())
        categorias_selecionadas = st.sidebar.multiselect(
            "Categorias:",
            options=categorias_disponiveis,
            default=categorias_disponiveis,
        )
        if categorias_selecionadas:
            df_filtrado = df_filtrado[
                df_filtrado["categoria"].isin(categorias_selecionadas)
            ]

    # Botão de atualizar
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Atualizar Dados", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    # Info na sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style="text-align: center; opacity: 0.5; font-size: 0.75rem;">
            💡 Os dados vêm da mesma tabela<br>
            usada pelo <code>financeiro.py</code>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return df_filtrado, titulo_periodo


# ========== PÁGINA PRINCIPAL ==========
def main():
    """Função principal do dashboard"""

    # Título
    st.markdown(
        '<p class="main-title">💰 Dashboard Financeiro Pessoal</p>',
        unsafe_allow_html=True,
    )

    # Carrega dados
    df = carregar_transacoes()

    if df.empty:
        st.warning("⚠ Nenhuma transação encontrada no banco de dados!")
        st.info(
            "👉 Use o programa `financeiro.py` no terminal para cadastrar suas primeiras transações."
        )
        st.stop()

    # Configura sidebar e obtém dados filtrados
    df_filtrado, titulo_periodo = configurar_sidebar(df)

    # Subtítulo do período
    st.markdown(f"### 📅 Período: **{titulo_periodo}**")
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    if df_filtrado.empty:
        st.warning("⚠ Nenhuma transação encontrada para o período selecionado.")
        st.info("Tente alterar os filtros na barra lateral.")
        return

    # ---- KPIs ----
    renderizar_kpis(df_filtrado)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ---- Gráficos Linha 1: Pizza de categorias ----
    col_esq, col_dir = st.columns(2)

    with col_esq:
        grafico_pizza_categorias(df_filtrado, tipo="Despesa")

    with col_dir:
        grafico_pizza_categorias(df_filtrado, tipo="Receita")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ---- Gráfico: Evolução do Saldo ----
    grafico_evolucao_saldo(df_filtrado)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ---- Gráficos Linha 2: Barras mensal + Ranking ----
    col_esq2, col_dir2 = st.columns(2)

    with col_esq2:
        grafico_barras_mensal(df_filtrado)

    with col_dir2:
        grafico_barras_categorias(df_filtrado)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ---- Tabela de transações ----
    st.markdown(
        '<p class="section-header">📋 Detalhamento das Transações</p>',
        unsafe_allow_html=True,
    )
    tabela_transacoes(df_filtrado)

    # Footer
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center; opacity: 0.4; font-size: 0.8rem; padding: 1rem;">
            Dashboard Financeiro Pessoal • Dados atualizados em {datetime.now().strftime("%d/%m/%Y às %H:%M")}
        </div>
        """,
        unsafe_allow_html=True,
    )


# Executa o dashboard
if __name__ == "__main__":
    main()
