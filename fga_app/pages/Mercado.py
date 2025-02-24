import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import date
from src.config.pages_config import Pages
from src.connection.database import engine
from src.config.trending_functions import detrending
from src.querys.querys_dictionary import (
    query_primeiro_contrato_acucar,
    query_contratos_ativos,
    query_reais_ton,
    query_reais_ton_primeiro_contrato,
    query_serie_inflacinada
    )



mercado = Pages(
    page= 'pages/mercado.py',
    title='Mercado'
)

mercado_page = mercado._page_setup()

dicionario_contratos = {
    'Primeiro Contrato' : 1,
    'Segundo Contrato' : 2, 
    'Terceiro Contrato' : 3, 
    'Quarto Contrato' : 4, 
    'Quinto Contrato': 5
}

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
    produtos = ["Açucar", "Soja", "Trigo", "Café"]

    # Widget para seleção do produto
    produto_selecionado = st.selectbox("Selecione um produto:", produtos)
    # Divisor estilizado
    st.markdown("---")

# Criar abas para diferentes tipos de conteúdo
tab1, tab2, tab3 = st.tabs(["📈 Gráficos", "📊 Tabela", "💾 Download"])

# Conteúdo da primeira aba (Gráficos)
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        contratos = st.selectbox(
            "Selecione um produto:",
            options=['All', 'Primeiro Contrato', 'Segundo Contrato', 'Terceiro Contrato', 'Quarto Contrato', 'Quinto Contrato']
            )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        data_inicio = st.date_input(
            label="Selecione data inicial da série:",
            value=pd.to_datetime("2023-01-01"),
            min_value=date(2000, 1, 1),
            key="data_inicio"
        )
        
    with col2:
        data_fim = st.date_input(
            label="Selecione data final da série:",
            value=pd.to_datetime("2024-01-01"),
            key="data_fim"
        )

    data_inicio_query = pd.to_datetime(data_inicio, dayfirst=True)
    data_fim_query = pd.to_datetime(data_fim, dayfirst=True)


    # Inicializar o session_state
if "filtro_reais_ton" not in st.session_state:
    st.session_state.filtro_reais_ton = False

if "filtro_tendencia" not in st.session_state:
    st.session_state.filtro_tendencia = False

# Widget do checkbox (DEVE VIR ANTES DA QUERY!)
filtro_reais_ton = st.checkbox("Reais/ Tonelada", value=st.session_state.filtro_reais_ton)
filtro_tendencia = st.checkbox("Remover Tendência", value = st.session_state.filtro_tendencia)

# Atualizar estado e rerun se necessário
if filtro_reais_ton != st.session_state.filtro_reais_ton:
    st.session_state.filtro_reais_ton = filtro_reais_ton
    st.rerun()

if filtro_tendencia != st.session_state.filtro_tendencia:
    st.session_state.filtro_tendencia = filtro_tendencia
    st.rerun()

# Lógica da query com base no filtro
if data_inicio_query <= data_fim_query:
    with engine.connect() as connection:
        if st.session_state.filtro_reais_ton:
            query = query_reais_ton_primeiro_contrato(data_inicio_query, data_fim_query,dicionario_contratos[contratos] )
        elif st.session_state.filtro_tendencia and st.session_state.filtro_reais_ton:
             query = query_serie_inflacinada(data_inicio_query, data_fim_query)
        else:
            if contratos == 'All':
                query = query_contratos_ativos(data_inicio_query, data_fim_query)
            else:
                query = query_primeiro_contrato_acucar(data_inicio_query, data_fim_query, dicionario_contratos[contratos])

        result = connection.execute(query)
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
        if st.session_state.filtro_tendencia and st.session_state.filtro_reais_ton:
            df = detrending(df)
        
else:
    st.error("Data inicial deve ser anterior à data final!")
    st.stop()

# Renderizar gráfico único (sem duplicação)
try:
    coluna_preco = "detrending" if st.session_state.filtro_tendencia else ("reais_ton" if st.session_state.filtro_reais_ton else "anterior")
    df[coluna_preco] = pd.to_numeric(df[coluna_preco], errors="coerce")
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("data:T", 
                axis=alt.Axis(
                    format="%d/%m/%Y",
                    title="Data",
                    labelAngle=-45
                ),
                ),
        y=alt.Y(f"{coluna_preco}:Q", 
                title="Preço (R$/ton)" if st.session_state.filtro_reais_ton else "Preço (cts/lp)"
                ),
        # color=alt.Color("nome_contrato:N", legend=alt.Legend(title="Contrato")),
        tooltip=[
            alt.Tooltip("data:T", format="%d/%m/%Y"),
            coluna_preco,
            "nome_contrato"
        ]
    ).properties(
        title="Preço de Contratos Agrícolas",
        height=700
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao gerar gráfico: {e}")


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
