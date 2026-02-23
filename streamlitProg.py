# Importação debibliotecas necessárias
import streamlit as st
import pandas as pd
import altair as alt

# Configuração da página do streamlit
st.set_page_config(
    page_title="Dashboard da alegria", layout="wide"  # Usa a largura completa da página
)

# Configuração do título da página e da bara lateral
st.title("Painel de vendas")

st.sidebar.header("Configurações de filtro")

# Criação de dados para simular vendas em alguns meses.
dados_vendas = pd.DataFrame(
    {
        "Mês": [
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
        ],
        "Vendas": [100, 150, 120, 200, 180, 250, 220, 190, 210, 230, 240, 260],
        "Meta": [150, 140, 130, 180, 180, 220, 210, 200, 220, 230, 240, 250],
    }
)

# Interatividade com a página
venda_minima = st.sidebar.slider(
    label="Exibir vendas a partir de: ", min_value=0, max_value=300, value=100
)

# Lógica da Filtragem
dados_filtrados = dados_vendas[dados_vendas["Vendas"] >= venda_minima]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tabela de dados filtrada")
    st.dataframe(dados_filtrados, use_container_width=True)

with col2:
    st.subheader("Visualização Gráfica")
    # Define a ordem correta dos meses para o gráfico
    ordem_meses = [
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
    # Transforma os dados para formato longo (necessário para Altair)
    dados_grafico = dados_filtrados.melt(
        id_vars="Mês",
        value_vars=["Vendas", "Meta"],
        var_name="Tipo",
        value_name="Valor",
    )
    grafico = (
        alt.Chart(dados_grafico)
        .mark_line(point=True)
        .encode(
            x=alt.X("Mês:N", sort=ordem_meses, title="Mês"),
            y=alt.Y("Valor:Q", title="Valor"),
            color=alt.Color("Tipo:N", title="Legenda"),
        )
        .properties(height=400)
    )
    st.altair_chart(grafico, use_container_width=True)

if not dados_filtrados.empty:
    melhor_mes = dados_filtrados.loc[dados_filtrados["Vendas"].idxmax(), "Mês"]
    st.success(f"Destaque: o melhor mês no filtro atual é: {melhor_mes}")
else:
    st.warning("Atenção! Nenhum dado atende aos critérios do filtro.")
