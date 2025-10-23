import pandas as pd
import streamlit as st
import plotly.express as px
import requests

# definindo wide mode
st.set_page_config(layout="wide")


# definindo função para formatar valores monetários
def formatar_valor(valor, prefixo):
    for unidade in ["", "mil"]:
        if valor <1000:
            return f"{prefixo} {valor:.2f} {unidade}"
        valor = valor / 1000
    return f"{prefixo} {valor:.2f} milhões"

# definindo titulo
st.title("Dashboard de Vendas :smile:")

# obtendo dados da API
url = 'https://labdados.com/produtos'
regioes = ['Brasil', 'Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']

# criando filtros na sidebar
st.sidebar.title('Filtros')
regiao = st.sidebar.selectbox('Região', regioes)

if regiao == 'Brasil':
    regiao = ''

todos_anos = st.sidebar.checkbox('Dados de todo o período', value = True)
if todos_anos:
    ano = ''
else:
    ano = st.sidebar.slider('Ano', 2020, 2023)

query_string = {'regiao':regiao.lower(), 'ano':ano}
response = requests.get(url, params= query_string)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

# criando filtro vendedores
filtro_vendedores = st.sidebar.multiselect('Vendedores', dados['Vendedor'].unique())
if filtro_vendedores:
    dados = dados[dados['Vendedor'].isin(filtro_vendedores)]


# definindo tabelas por receitas
## TABELA DE REGIÃO DE VENDAS
regiao_vendas = dados.groupby('Local da compra')['Preço'].sum()
regiao_vendas = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(regiao_vendas, left_on='Local da compra', right_index=True)
## TABELA DE RECEITA MENSAL
receita_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
receita_mensal['Ano'] = receita_mensal['Data da Compra'].dt.year
receita_mensal['Mes'] = receita_mensal['Data da Compra'].dt.month_name()
## TABELA DE RECEITA POR CATEGORIA
receita_categoria = dados.groupby('Categoria do Produto')['Preço'].sum()
## TABELA DE VENDEDORES
vendedores = pd.DataFrame(dados.groupby('Vendedor')['Preço'].agg(['sum', 'count']))

# definindo tabelas por quantidades
## TABELA DE REGIÃO DE VENDAS POR QUANTIDADE
regiao_quantidade = dados.groupby('Local da compra')['Produto'].count()
regiao_quantidade = dados.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(regiao_quantidade, left_on='Local da compra', right_index=True)
## TABELA DE QUANTIDADE DE VENDAS MENSAIS
quantidade_mensal = dados.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Produto'].count().reset_index()
quantidade_mensal['Ano'] = quantidade_mensal['Data da Compra'].dt.year
quantidade_mensal['Mes'] = quantidade_mensal['Data da Compra'].dt.month_name()
## TABELA ESTADOS COM MAIS QUANTIDADE DE VENDAS
estados_quantidade = dados.groupby('Local da compra')['Produto'].count().sort_values(ascending=False)
## TABELA CATEGORIAS COM MAIS QUANTIDADE DE VENDAS
categorias_quantidade = dados.groupby('Categoria do Produto')['Produto'].count().sort_values(ascending=False)

# criando grafico de mapa de vendas por regiao
fig_mapa = px.scatter_geo(
    regiao_vendas,
    lat='lat',
    lon='lon',
    scope='south america',
    size='Preço',
    hover_name='Local da compra',
    hover_data={'lat':False, 'lon':False, 'Preço':':.2f'},
    color_discrete_sequence=['blue'],
    template='seaborn',
    title='Vendas por Região')

# criando grafico de linha de receita mensal
fig_receita_mensal = px.line(
    receita_mensal,
    x='Mes',
    y='Preço',
    title='Receita Mensal',
    labels={'Preço':'Receita', 'Mes':'Mês'},
    template='seaborn',
    markers=True,
    range_y=[50000, receita_mensal['Preço'].max() * 1.1],
    color='Ano',
    line_dash='Ano')

# criando grafico de barras por estado com mais receita
fig_receita_estados = px.bar(regiao_vendas.head(),
                             x='Local da compra',
                             y='Preço',
                             title='Top 5 Estados por Receita',
                             labels={'Preço':'Receita', 'Local da compra':'Estado'},
                             template='seaborn')

# criando grafico de barras por categoria com mais receita
fig_receita_categoria = px.bar(receita_categoria,
                               text_auto=True,
                               title='Receita por Categoria',
                               labels={'Preço':'Receita', 'index':'Categoria'},
                               template='seaborn')

# criando grafico de região por quantidade de vendas
fig_mapa_quantidade = px.scatter_geo(regiao_quantidade,
                                    lat='lat',
                                    lon='lon',
                                    scope='south america',
                                    size='Produto',
                                    hover_name='Local da compra',
                                    hover_data={'lat':False, 'lon':False, 'Produto':':.0f'},
                                    color_discrete_sequence=['blue'],
                                    template='seaborn',
                                    title='Quantidade de Vendas por Região')

# criando grafico de linha de quantidade mensal
fig_quantidade_mensal = px.line(quantidade_mensal,
                                x='Mes',
                                y='Produto',
                                title='Quantidade de Vendas Mensais',
                                labels={'Produto':'Quantidade de Vendas', 'Mes':'Mês'},
                                template='seaborn',
                                markers=True,
                                range_y=[150, quantidade_mensal['Produto'].max() * 1.1],
                                color='Ano',
                                line_dash='Ano')

# criando grafico de barras por estado com mais quantidade de vendas
fig_quantidade_estados = px.bar(estados_quantidade.head(5).reset_index(),
                                 x='Local da compra',
                                 y='Produto',
                                 title='Top 5 Estados por Quantidade de Vendas',
                                 labels={'Produto':'Quantidade de Vendas', 'Local da compra':'Estado'},
                                 template='seaborn')


fig_quantidade_categorias = px.bar(categorias_quantidade.head(5).reset_index(),
                                 x='Categoria do Produto',
                                 y='Produto',
                                 title='Top 5 Categorias por Quantidade de Vendas',
                                 labels={'Produto':'Quantidade de Vendas', 'Categoria do Produto':'Categoria'},
                                 template='seaborn')

# colocando principais metricas

# criando abas no streamlit
tab1, tab2, tab3 = st.tabs(["Visão Geral", "Quantidades", "Vendedores"])
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Receita Total", formatar_valor(dados["Preço"].sum(), "R$"))
        st.plotly_chart(fig_mapa, use_container_width=True)
        st.plotly_chart(fig_receita_estados, use_container_width=True)
    with col2:
        st.metric("Número de Pedidos", formatar_valor(dados.shape[0], ""))
        st.plotly_chart(fig_receita_mensal, use_container_width=True)
        st.plotly_chart(fig_receita_categoria, use_container_width=True)
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Receita Total", formatar_valor(dados["Preço"].sum(), "R$"))
        st.plotly_chart(fig_mapa_quantidade, use_container_width=True)
        st.plotly_chart(fig_quantidade_estados, use_container_width=True)
    with col2:
        st.metric("Número de Pedidos", formatar_valor(dados.shape[0], ""))
        st.plotly_chart(fig_quantidade_mensal, use_container_width=True)
        st.plotly_chart(fig_quantidade_categorias, use_container_width=True)
with tab3:
    qtd_vendedores = st.number_input("Vendedores", 2, 10, 5)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Receita Total", formatar_valor(dados["Preço"].sum(), "R$"))
        fig_vendedores_receita = px.bar(vendedores[['sum']].sort_values('sum', ascending=False).head(qtd_vendedores),
                                        x='sum',
                                        y=vendedores[['sum']].sort_values('sum', ascending=False).head(qtd_vendedores).index,
                                        title=f'Tops {qtd_vendedores} Vendedores por Receita',
                                        labels={'sum':'Receita', 'index':'Vendedor'},
                                        template='seaborn',
                                        text_auto=True)
        st.plotly_chart(fig_vendedores_receita, use_container_width=True)
    with col2:
        st.metric("Número de Pedidos", formatar_valor(dados.shape[0], ""))
        fig_vendedores_pedidos = px.bar(vendedores[['count']].sort_values('count', ascending=False).head(qtd_vendedores),
                                        x='count',
                                        y=vendedores[['count']].sort_values('count', ascending=False).head(qtd_vendedores).index,                                       
                                        title=f'Tops {qtd_vendedores} Vendedores por Número de Pedidos',
                                        labels={'count':'Número de Pedidos', 'index':'Vendedor'},
                                        template='seaborn',
                                        text_auto=True)
        st.plotly_chart(fig_vendedores_pedidos, use_container_width=True)

    








