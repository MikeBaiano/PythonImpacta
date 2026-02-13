# Importação debibliotecas necessárias
import streamlit as st
import pandas as pd

# Configuração da página do streamlit
st.set_page_config(
    page_title = 'Dashboard da alegria',
    layout = 'wide' # Usa a largura completa da página
)

# Configuração do título da página e da bara lateral
st.title('Painel de vendas')

st.sidebar.header('Configurações de filtro')

# Criação de dados para simular vendas em alguns meses.
dados_vendas = pd.DataFrame({
    'Mês':   ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    'Vendas':[100, 150, 120, 200, 180, 250],
    'Meta':  [150, 140, 130, 180, 180, 220]
})

# Interatividade com a página
venda_minima = st.sidebar.slider(
    label = 'Exibir vendas a partir de: ',
    min_value = 0,
    max_value = 300,
    value = 100
)

# Lógica da Filtragem
dados_filtrados = dados_vendas[dados_vendas['Vendas'] >= venda_minima]

col1, col2 = st.columns(2)

with col1:
    st.subheader('Tabela de dados filtrada')
    st.dataframe(dados_filtrados, use_container_width = True)

with col2:
    st.subheader('Visualização Gráfica')
    st.line_chart(dados_filtrados.set_index('Mês'))

if not dados_filtrados.empty:
    melhor_mes = dados_filtrados.loc[dados_filtrados['Vendas'].idxmax(), 'Mês']
    st.success(f'Destaque: o melhor mês no filtro atual é: {melhor_mes}')
else:
    st.warning('Atenção! Nenhum dado atende aos critérios do filtro.')
    
