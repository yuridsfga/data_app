import streamlit as st


class Pages:
    def __init__(self, page: str, title: str):
        '''
        page: url da pagina em questao, ex: 'pages/nome_da_pagina.py'
        title: titulo da pagina em questao.
        '''
        self.page = page
        self.title = title

    
    def _page_setup(self):
        '''
        Definie setups da pagina.
        
        '''
        page = st.set_page_config(
            page_title=self.title,
            page_icon="🚀",
            layout="wide"
            )


        return page
    
