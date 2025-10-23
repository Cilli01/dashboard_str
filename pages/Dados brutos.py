import pandas as pd
import streamlit as st
import requests
import time

@st.cache_data

# definindo função para baixar planilha
def baixar_planilha(df):
    return df.to_csv(index=False).encode('utf-8')

# definindo mensagem de sucesso
def mensagem_sucesso():
    sucesso = st.success('Dowloado do arquivo concluido com sucesso!')
    time.sleep(10)
    sucesso.empty()

# definindo titulo
st.title("Dados Brutos")

# obtendo dados da API
url = 'https://labdados.com/produtos'
response = requests.get(url)
dados = pd.DataFrame.from_dict(response.json())
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format = '%d/%m/%Y')

# filtrando colunas da tabela
with st.expander('Colunas'):
    colunas = st.multiselect('Selecione Colunas', list(dados.columns), list(dados.columns))

# criando o sidebar e filtros laterais
st.sidebar.title('Filtros da Tabela')

with st.sidebar.expander('Produtos'):
    # filtro por produto
    produtos = st.multiselect('Produtos', dados['Produto'].unique(), dados['Produto'].unique())
    # filtro por categoria
with st.sidebar.expander('Categorias'):     
    categorias = st.multiselect('Categorias', dados['Categoria do Produto'].unique(), dados['Categoria do Produto'].unique())
    # filtro por preço
with st.sidebar.expander('Preços'):    
    preco = st.slider('Preço', float(dados['Preço'].min()), float(dados['Preço'].max()), (float(dados['Preço'].min()), float(dados['Preço'].max())))
    # filtro por vendedor
with st.sidebar.expander('Vendedores'):    
    vendedor = st.multiselect('Vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())
    # filtro por região
with st.sidebar.expander('Estados/Regiões'):    
    regiao = st.multiselect('Regiões', dados['Local da compra'].unique(), dados['Local da compra'].unique())
    # filtro por avaliação
with st.sidebar.expander('Avaliação'):    
    avaliacao = st.slider('Avaliação', int(dados['Avaliação da compra'].min()), int(dados['Avaliação da compra'].max()), (int(dados['Avaliação da compra'].min()), int(dados['Avaliação da compra'].max())))
    # filtro por tipo de pagamento
with st.sidebar.expander('Tipo de Pagamento'):    
    pagamento = st.multiselect('Tipo de pagamento', dados['Tipo de pagamento'].unique(), dados['Tipo de pagamento'].unique())
    # filtro por data
with st.sidebar.expander('Data da Compra'):    
    data_compra = st.date_input('Data da compra', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))

# criando a query de filtros
query = 'Produto in @produtos' \
' and `Categoria do Produto` in @categorias' \
' and @preco[0] <= Preço <= @preco[1]' \
' and Vendedor in @vendedor' \
' and `Local da compra` in @regiao' \
' and @avaliacao[0] <= `Avaliação da compra` <= @avaliacao[1]' \
' and `Tipo de pagamento` in @pagamento' \
' and @data_compra[0] <= `Data da Compra` <= @data_compra[1]'

dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

# exibindo dados brutos
st.dataframe(dados_filtrados)
st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]} colunas]')

st.markdown('Defina o nome do arquivo para baixar a planilha')

coluna_1, coluna_2 = st.columns(2)
with coluna_1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados_brutos')
    nome_arquivo+= '.csv'
with coluna_2:
    st.download_button('Baixar Dados', data=baixar_planilha(dados_filtrados), file_name=nome_arquivo, mime='text/csv', on_click=mensagem_sucesso)
