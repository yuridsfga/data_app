import streamlit as st


st.set_page_config(
    page_title="FG/A_Data 🌾",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com',
        'Report a bug': "https://www.example.com",
        'About': "App de análise de commodities agrícolas."
    }
)

col1, col2 = st.columns([1, 4])
with col1:
    st.image('C:/Users/YuriSaneripCalzzani/Documents/GitHub/data_app/fga_app/src/images/fga_logo_png.png', width=150) # Substitua pelo link da sua logo



# CSS personalizado para o tema agrícola
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

# Conteúdo principal
st.title("FG/A:")
st.header("  Centro de Dados")

st.markdown("""
O Centro de Dados FG/ A funciona como uma central de distribuição de dados estratégicos para análise de mercado. 
Nosso objetivo é fornecer informações atualizadas, precisas e acessíveis para apoiar a tomada de decisões no agronegócio.

Principais Funcionalidades:
""")
funcionalidades = """
    ✅ Acesso a Dados de Mercado – Informações sobre preços de commodities, tendências de mercado, variações sazonais e indicadores econômicos.

    ✅ Relatórios Personalizados – Geração de relatórios automatizados e dashboards interativos para visualização estratégica.

    ✅ Integração com Fontes Oficiais – Conexão com bancos de dados de órgãos reguladores, cooperativas e entidades do setor.

    ✅ API para Integração – Possibilidade de integrar os dados diretamente a sistemas de gestão e plataformas analíticas.
"""

st.markdown(funcionalidades)










