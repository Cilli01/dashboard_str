# 🧭 Dashboard de Vendas - Streamlit

Este projeto é um **Dashboard de Vendas interativo**, desenvolvido com **Python**, **Streamlit**, **Plotly** e **Pandas**.  
O objetivo é permitir a **análise de vendas e desempenho comercial** de forma visual e dinâmica, consumindo dados reais a partir de uma **API pública**.

---

## 📊 Funcionalidades

### **Página: Dashboard de Vendas**
Esta é a página principal do projeto, onde é possível:
- Filtrar dados por **região**, **ano** e **vendedores**;  
- Visualizar **mapas interativos de vendas** por localidade;  
- Acompanhar **gráficos de receita e volume de vendas mensais**;  
- Analisar os **Top 5 estados** e **categorias** com maior desempenho;  
- Consultar os **vendedores com maiores receitas e número de pedidos**.  

Gráficos e métricas são atualizados dinamicamente conforme os filtros aplicados.

---

### **Página: Dados Brutos**
Esta página fornece uma visão detalhada e personalizável dos dados de vendas, permitindo:
- Selecionar quais **colunas** visualizar na tabela;  
- Aplicar filtros por **produto**, **categoria**, **preço**, **vendedor**, **região**, **avaliação**, **tipo de pagamento** e **data da compra**;  
- Baixar os dados filtrados em formato **CSV**.  

---

## 🧩 Tecnologias Utilizadas

| Biblioteca | Descrição |
|-------------|------------|
| **Streamlit** | Criação do dashboard interativo |
| **Pandas** | Manipulação e tratamento de dados |
| **Plotly Express** | Criação de gráficos interativos |
| **Requests** | Consumo da API de dados externos |

---

## ⚙️ Instalação e Execução Local

### **Clonar o repositório**
```bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
cd NOME-DO-REPOSITORIO

# Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# Instalar dependências
pip install -r requirements.txt

Executar o aplicativo Streamlit
streamlit run Dashboard.py

Após executar o comando acima, o navegador abrirá automaticamente o dashboard na URL:

http://localhost:8501

📁 Projeto-Dashboard-Vendas/
│
├── Dashboard.py           # Página principal do dashboard
├── Dados brutos.py        # Página com os dados filtráveis e download
├── requirements.txt       # Dependências do projeto
└── README.md              # Documentação do projeto

Fonte de Dados

Os dados são obtidos a partir da API pública:

https://labdados.com/produtos

```bash

Autor

Caio Cesar
Desenvolvedor e Analista de Dados
📧 caiocesarccs01@gmail.com
💻 www.linkedin.com/in/caio-cesar-60234a277
