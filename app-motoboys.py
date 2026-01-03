"""
Sistema de Controle de Motoboys
Aplicação web para substituir planilha Excel com interface operacional e gerencial

Versão 2026 - Otimizada para Streamlit Cloud
- Gemini 1.5 Flash (via google-genai)
- Supabase 2.x
- Correção Definitiva de Largura (width='stretch')
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
            
            # CORREÇÃO: width='stretch' substitui use_container_width
            submitted = st.form_submit_button("✅ Registrar", width='stretch')

            if submitted and nome:
                if db.inserir_registro(nome.strip(), data_registro, periodo, tipo, entregas):
                    st.success(f"✅ Registro de {nome} adicionado!")
                    st.rerun()

    with col2:
        st.subheader("📅 Registros de Hoje")
        registros_hoje = db.buscar_registros_dia(date.today())
        if registros_hoje:
            for registro in registros_hoje:
                col_info, col_actions = st.columns([3, 1])
                with col_info:
                    st.write(f"**{registro['nome']}** | {registro['periodo']} | 📦 {registro['entregas']} ent.")
                with col_actions:
                    c_edit, c_del = st.columns(2)
                    if c_edit.button("✏️", key=f"edit_{registro['id']}"):
                        st.session_state.editando_registro = registro
                    if c_del.button("🗑️", key=f"del_{registro['id']}"):
                        if db.excluir_registro(registro['id']): st.rerun()
                st.divider()
        else:
            st.info("ℹ️ Nenhum registro hoje.")

# ==================== ABA GERENCIAL ====================
with tab_gerencial:
    st.header("Análise Gerencial e IA")
    config_atual = db.buscar_configuracao_ativa()
    kpis_hoje = db.calcular_kpis_dia(date.today())
    relatorio_semanal = db.gerar_relatorio_semanal()

    with st.expander("🔧 Gerenciar Valores", expanded=False):
        col_c1, col_c2, col_c3 = st.columns([2, 2, 1])
        v_diaria = col_c1.text_input("Diária (R$)", value=f"{config_atual.get('valor_diaria', 0):.2f}".replace('.', ','))
        v_corrida = col_c2.text_input("Corrida (R$)", value=f"{config_atual.get('valor_corrida', 0):.2f}".replace('.', ','))
        
        # CORREÇÃO: width='stretch'
        if col_c3.button("💾 Salvar", width='stretch'):
            if db.salvar_configuracao(utils.parse_moeda(v_diaria), utils.parse_moeda(v_corrida)):
                st.rerun()

    # KPIs
    st.subheader("📈 Indicadores de Hoje")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📦 Entregas", kpis_hoje['total_entregas'])
    c2.metric("🏍️ Motoboys", kpis_hoje['total_motoboys'])
    c3.metric("📊 Média", f"{kpis_hoje['media_entregas_moto']:.1f}")
    c4.metric("💰 Custo", utils.formatar_moeda(kpis_hoje['custo_total']))
    c5.metric("💵 Por Entrega", utils.formatar_moeda(kpis_hoje['custo_medio_entrega']))

    st.divider()

    # Relatório Semanal
    if relatorio_semanal:
        df_relatorio = pd.DataFrame(relatorio_semanal)
        df_display = df_relatorio[['nome', 'tipo', 'dias_trabalhados', 'total_entregas', 'valor_devido']].copy()
        df_display['valor_devido'] = df_display['valor_devido'].apply(utils.formatar_moeda)
        
        # CORREÇÃO: width='stretch'
        st.dataframe(df_display, width='stretch', hide_index=True)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_entregas = px.bar(df_relatorio, x='nome', y='total_entregas', color='tipo', title='Entregas/Semana')
            st.plotly_chart(fig_entregas, width='stretch')
        with col_g2:
            df_fixos = df_relatorio[df_relatorio['tipo'] == 'Fixo']
            if not df_fixos.empty:
                fig_valores = px.bar(df_fixos, x='nome', y='valor_devido', title='Valores/Fixos', color_discrete_sequence=['#2ca02c'])
                st.plotly_chart(fig_valores, width='stretch')

    st.divider()

    # Assistente de IA
    st.subheader("🤖 Assistente de IA - Gemini 1.5 Flash")
    col_chat, col_sugestoes = st.columns([2, 1])

    with col_sugestoes:
        st.write("**💡 Sugestões:**")
        for p in ai_assistant.sugerir_perguntas():
            # CORREÇÃO: width='stretch'
            if st.button(p, key=f"sug_{p[:15]}", width='stretch'):
                st.session_state.chat_history.append({"role": "user", "message": p})
                res = ai_assistant.get_gemini_response(p, kpis_hoje, relatorio_semanal, config_atual)
                st.session_state.chat_history.append({"role": "assistant", "message": res})
                st.rerun()

    with col_chat:
        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["message"])
        
        user_input = st.chat_input("Pergunte sobre os dados...")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "message": user_input})
            with st.spinner("🤔 Analisando..."):
                res = ai_assistant.get_gemini_response(user_input, kpis_hoje, relatorio_semanal, config_atual)
            st.session_state.chat_history.append({"role": "assistant", "message": res})
            st.rerun()

st.divider()
st.markdown("<div style='text-align: center; color: #666;'>🏍️ Sistema Motoboys 2026</div>", unsafe_allow_html=True)
