import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
from src.config.pages_config import Pages
from src.connection.database import engine
from src.querys.queys_dictionary import query_primeiro_contrato_acucar



mercado = Pages(
    page= 'pages/mercado.py',
    title='Mercado'
)

mercado_page = mercado._page_setup()

# CSS personalizado para o tema agrícola
st.markdown("""
    <style>

        /* Importa a fonte do Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans&display=swap');

        /* Aplica a fonte para todo o conteúdo da página */
        html, body, [data-testid="stAppViewContainer"], .stApp {
            font-family: 'IBM Plex Sans', sans-serif;
        }
            

        /* Cores principais */
        :root {
            --primary: #99b27f; /* Verde */
            --secondary: #a7b99e; /* Verde claro */
            --background: #F1F8E9; /* Bege claro */
            --text: #2E7D32; /* Verde escuro */
        }

        /* Cor de fundo do app */
        .stApp {
            background-color: var(--background);
        }

        /* Cor do texto */
        .stTextInput > label, .stNumberInput > label, .stSelectbox > label, .stSlider > label, .stRadio > label {
            color: var(--text) !important;
        }

        /* Botões */
        .stButton > button {
            background-color: var(--primary) !important;
            color: white !important;
            border-radius: 10px !important;
            border: none !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: var(--secondary) !important;
        }

        /* Títulos */
        h1, h2, h3 {
            color: var(--text) !important;
        }
            
       /* Oculta completamente o header */
        [data-testid="stHeader"] {
            display: none;
        }
    
         /* Oculta o menu de 3 linhas (hamburger) */
        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    # Logo e título do menu
    st.markdown("## Navegação")

    # Lista de produtos disponíveis
    produtos = ["Açucar", "Milho", "Trigo", "Café"]

    # Widget para seleção do produto
    produto_selecionado = st.selectbox("Selecione um produto:", produtos)
    # Divisor estilizado
    st.markdown("---")

# Criar abas para diferentes tipos de conteúdo
tab1, tab2, tab3 = st.tabs(["📈 Gráficos", "📊 Tabela", "💾 Download"])

with engine.connect() as connection:
    result = connection.execute(query_primeiro_contrato_acucar)
    df = pd.DataFrame(result.fetchall(), columns=result.keys())

try:
    df["anterior"] = pd.to_numeric(df["anterior"], errors="coerce")
except Exception as e:
    st.error(f"Erro ao converter coluna: {e}")

# Conteúdo da primeira aba (Gráficos)
with tab1:
    st.header(f"Preço Mensal - {produto_selecionado}")
    
    chart = alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("data:T", 
            title="Data",
            axis=alt.Axis(
                format="%d/%m/%Y",
                title="Data",
                labelAngle=-45
            )
            ),
    y=alt.Y("anterior:Q", 
            title="Preço (cts/lp)",
            scale=alt.Scale(domain=[20, 22])
            ),
    color=alt.Color("nome_contrato:N", 
                    legend=alt.Legend(title="Contrato")
            ),
    tooltip=[
         alt.Tooltip("data:T", format="%d/%m/%Y"),  # Formato no tooltip também
        "anterior",
        "nome_contrato"
    ]
    ).properties(
    title="Preço de Contratos Agrícolas",
    height=400
    ).interactive() # Permite zoom/pan
    

    st.altair_chart(chart, use_container_width=True)

# Conteúdo da segunda aba (Tabela)
with tab2:
    st.header(f"Dados Brutos - {produto_selecionado}")
    st.dataframe(df, hide_index=True, width= 700)

# Conteúdo da terceira aba (Download)
with tab3:
    st.header(f"Download dos Dados - {produto_selecionado}")
    
    # Converter DataFrame para CSV
    csv = df.to_csv(index=False).encode("utf-8")
    
    # Botão de download
    st.download_button(
        label="Baixar CSV",
        data=csv,
        file_name=f"dados_{produto_selecionado.lower()}.csv",
        mime="text/csv",
    )
# # Redirecionamento para a página selecionada
# if pagina == "🏠 Home":
#     st.write("Esta é a página inicial.")
# elif pagina == "📊 Visão Geral":
#     st.switch_page("pages/overview.py")
# elif pagina == "📈 Análises":
#     st.switch_page("pages/analytics.py")

