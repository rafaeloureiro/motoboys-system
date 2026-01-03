"""
Sistema de Controle de Motoboys
Aplicação web para substituir planilha Excel com interface operacional e gerencial

Versão 2026 - Otimizada para Streamlit Cloud
- Gemini 1.5 Flash (via google-genai)
- Supabase 2.x
- Correção de largura (width='stretch')
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import database as db
import utils
import ai_assistant

# Configuração da página
st.set_page_config(
    page_title="Controle de Motoboys",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Verificar configuração de secrets
try:
    if "supabase" not in st.secrets or "google" not in st.secrets:
        st.error("""
        ⚠️ **Configuração Necessária**
        Por favor, configure os secrets no Streamlit Cloud (Settings > Secrets).
        """)
        st.stop()
except Exception as e:
    st.error(f"⚠️ **Erro de Configuração:** {str(e)}")
    st.stop()

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🏍️ Sistema de Controle de Motoboys</h1>', unsafe_allow_html=True)

# Inicializar session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'editando_registro' not in st.session_state:
    st.session_state.editando_registro = None

# Criar tabs principais
tab_operacional, tab_gerencial = st.tabs(["📋 OPERACIONAL", "📊 GERENCIAL"])

# ==================== ABA OPERACIONAL ====================
with tab_operacional:
    st.header("Gestão Operacional Diária")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("➕ Novo Registro")
        with st.form("form_registro", clear_on_submit=True):
            lista_motoboys = db.buscar_nomes_motoboys()
            
            if lista_motoboys:
                nome_selecionado = st.selectbox(
                    "Nome do Motoboy",
                    options=[""] + lista_motoboys + ["➕ Novo motoboy"],
                    index=0
                )
                nome = st.text_input("Nome (se novo)") if nome_selecionado in ["", "➕ Novo motoboy"] else nome_selecionado
            else:
                nome = st.text_input("Nome do Motoboy")

            data_registro = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
            col_p, col_t = st.columns(2)
            with col_p: periodo = st.selectbox("Período", ["Manhã", "Noite"])
            with col_t: tipo = st.selectbox("Tipo", ["Fixo", "Freelancer"])
            
            entregas = st.number_input("Entregas", min_value=0, value=0, step=1)
            # CORREÇÃO: use_container_width -> width='stretch'
            submitted = st.form_submit_button("✅ Registrar", width='stretch')

            if submitted and nome:
                if db.inserir
