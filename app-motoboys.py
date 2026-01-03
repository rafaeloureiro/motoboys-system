"""
Sistema de Controle de Motoboys
Aplicação web para substituir planilha Excel com interface operacional e gerencial

Versão 2026 - Otimizada para Streamlit Cloud
- Gemini 2.5 Flash
- Supabase 2.x
- Cache otimizado
- Pandas/Plotly atualizados
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    # Verificar se secrets estão configurados
    if "supabase" not in st.secrets or "google" not in st.secrets:
        st.error("""
        ⚠️ **Configuração Necessária**

        Por favor, configure os secrets no Streamlit Cloud:

        1. Vá em **Settings** > **Secrets**
        2. Adicione o seguinte conteúdo:

        ```toml
        [supabase]
        url = "https://sttpygyknnuqrdfuzfph.supabase.co"
        key = "SUA_SUPABASE_KEY"

        [google]
        api_key = "SUA_GOOGLE_API_KEY"
        ```

        Consulte o arquivo `DEPLOY.md` para instruções detalhadas.
        """)
        st.stop()
except Exception as e:
    st.error(f"""
    ⚠️ **Erro de Configuração**

    Não foi possível carregar as configurações (secrets).

    **Para desenvolvimento local:**
    - Certifique-se de que o arquivo `.streamlit/secrets.toml` existe
    - Preencha com suas credenciais do Supabase e Google

    **Para Streamlit Cloud:**
    - Configure os secrets em Settings > Secrets

    **Erro:** {str(e)}
    """)
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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
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

    # Coluna 1: Formulário de Registro
    with col1:
        st.subheader("➕ Novo Registro")

        with st.form("form_registro", clear_on_submit=True):
            # Buscar lista de motoboys para autocomplete
            lista_motoboys = db.buscar_nomes_motoboys()

            # Campo nome com autocomplete
            if lista_motoboys:
                nome_selecionado = st.selectbox(
                    "Nome do Motoboy",
                    options=[""] + lista_motoboys + ["➕ Novo motoboy"],
                    index=0
                )

                if nome_selecionado == "➕ Novo motoboy":
                    nome = st.text_input("Digite o nome do novo motoboy")
                elif nome_selecionado == "":
                    nome = st.text_input("Ou digite um nome")
                else:
                    nome = nome_selecionado
            else:
                nome = st.text_input("Nome do Motoboy")

            data_registro = st.date_input(
                "Data",
                value=date.today(),
                format="DD/MM/YYYY"
            )

            col_periodo, col_tipo = st.columns(2)

            with col_periodo:
                periodo = st.selectbox("Período", ["Manhã", "Noite"])

            with col_tipo:
                tipo = st.selectbox("Tipo", ["Fixo", "Freelancer"])

            entregas = st.number_input(
                "Número de Entregas",
                min_value=0,
                value=0,
                step=1
            )

            submitted = st.form_submit_button("✅ Registrar", use_container_width=True)

            if submitted:
                if nome and nome.strip():
                    sucesso = db.inserir_registro(
                        nome.strip(),
                        data_registro,
                        periodo,
                        tipo,
                        entregas
                    )

                    if sucesso:
                        st.success(f"✅ Registro de {nome} adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar registro. Verifique a conexão com o banco de dados.")
                else:
                    st.warning("⚠️ Por favor, preencha o nome do motoboy.")

    # Coluna 2: Listagem do Dia
    with col2:
        st.subheader("📅 Registros de Hoje")

        registros_hoje = db.buscar_registros_dia(date.today())

        if registros_hoje:
            # Exibir cada registro em um card
            for registro in registros_hoje:
                with st.container():
                    col_info, col_actions = st.columns([3, 1])

                    with col_info:
                        tipo_emoji = "🔧" if registro['tipo'] == "Fixo" else "🏍️"
                        periodo_emoji = "☀️" if registro['periodo'] == "Manhã" else "🌙"

                        st.markdown(f"""
                        **{tipo_emoji} {registro['nome']}** | {periodo_emoji} {registro['periodo']} | 📦 {registro['entregas']} entregas
                        """)

                    with col_actions:
                        col_edit, col_del = st.columns(2)

                        with col_edit:
                            if st.button("✏️", key=f"edit_{registro['id']}", help="Editar"):
                                st.session_state.editando_registro = registro

                        with col_del:
                            if st.button("🗑️", key=f"del_{registro['id']}", help="Excluir"):
                                if db.excluir_registro(registro['id']):
                                    st.success("✅ Registro excluído!")
                                    st.rerun()
                                else:
                                    st.error("❌ Erro ao excluir registro.")

                    st.divider()
        else:
            st.info("ℹ️ Nenhum registro encontrado para hoje.")

    # Modal de edição
    if st.session_state.editando_registro:
        registro = st.session_state.editando_registro

        st.divider()
        st.subheader("✏️ Editar Registro")

        with st.form("form_edicao"):
            nome_edit = st.text_input("Nome do Motoboy", value=registro['nome'])

            data_edit = st.date_input(
                "Data",
                value=datetime.strptime(registro['data'], '%Y-%m-%d').date(),
                format="DD/MM/YYYY"
            )

            col_periodo_edit, col_tipo_edit = st.columns(2)

            with col_periodo_edit:
                periodo_index = 0 if registro['periodo'] == "Manhã" else 1
                periodo_edit = st.selectbox("Período", ["Manhã", "Noite"], index=periodo_index)

            with col_tipo_edit:
                tipo_index = 0 if registro['tipo'] == "Fixo" else 1
                tipo_edit = st.selectbox("Tipo", ["Fixo", "Freelancer"], index=tipo_index)

            entregas_edit = st.number_input(
                "Número de Entregas",
                min_value=0,
                value=registro['entregas'],
                step=1
            )

            col_salvar, col_cancelar = st.columns(2)

            with col_salvar:
                salvar = st.form_submit_button("💾 Salvar", use_container_width=True)

            with col_cancelar:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)

            if salvar:
                if db.atualizar_registro(
                    registro['id'],
                    nome_edit,
                    data_edit,
                    periodo_edit,
                    tipo_edit,
                    entregas_edit
                ):
                    st.success("✅ Registro atualizado com sucesso!")
                    st.session_state.editando_registro = None
                    st.rerun()
                else:
                    st.error("❌ Erro ao atualizar registro.")

            if cancelar:
                st.session_state.editando_registro = None
                st.rerun()

# ==================== ABA GERENCIAL ====================
with tab_gerencial:
    st.header("Análise Gerencial e IA")

    # Buscar dados
    config_atual = db.buscar_configuracao_ativa()
    kpis_hoje = db.calcular_kpis_dia(date.today())
    relatorio_semanal = db.gerar_relatorio_semanal()

    # SEÇÃO A: Configurações
    st.subheader("⚙️ Configurações Globais")

    with st.expander("🔧 Gerenciar Valores", expanded=False):
        col_config1, col_config2, col_config3 = st.columns([2, 2, 1])

        with col_config1:
            valor_diaria_str = st.text_input(
                "Valor da Diária (R$)",
                value=f"{config_atual.get('valor_diaria', 0):.2f}".replace('.', ','),
                help="Use formato: 150,00"
            )

        with col_config2:
            valor_corrida_str = st.text_input(
                "Valor por Corrida (R$)",
                value=f"{config_atual.get('valor_corrida', 0):.2f}".replace('.', ','),
                help="Use formato: 5,50"
            )

        with col_config3:
            st.write("")  # Espaçamento
            st.write("")  # Espaçamento
            if st.button("💾 Salvar Configurações", use_container_width=True):
                valor_diaria = utils.parse_moeda(valor_diaria_str)
                valor_corrida = utils.parse_moeda(valor_corrida_str)

                if db.salvar_configuracao(valor_diaria, valor_corrida):
                    st.success("✅ Configurações salvas com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Erro ao salvar configurações.")

        # Exibir valores atuais
        st.info(f"""
        📌 **Valores Ativos:**
        - Diária: {utils.formatar_moeda(config_atual.get('valor_diaria', 0))}
        - Corrida: {utils.formatar_moeda(config_atual.get('valor_corrida', 0))}
        """)

    st.divider()

    # SEÇÃO B: KPIs do Dia
    st.subheader("📈 Indicadores de Hoje")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="📦 Total Entregas",
            value=kpis_hoje['total_entregas']
        )

    with col2:
        st.metric(
            label="🏍️ Total Motoboys",
            value=kpis_hoje['total_motoboys']
        )

    with col3:
        st.metric(
            label="📊 Média Entregas/Moto",
            value=f"{kpis_hoje['media_entregas_moto']:.1f}"
        )

    with col4:
        st.metric(
            label="💰 Custo Total",
            value=utils.formatar_moeda(kpis_hoje['custo_total'])
        )

    with col5:
        st.metric(
            label="💵 Custo/Entrega",
            value=utils.formatar_moeda(kpis_hoje['custo_medio_entrega'])
        )

    st.divider()

    # SEÇÃO C: Relatório Semanal
    st.subheader("📅 Relatório Semanal (Segunda até Hoje)")

    if relatorio_semanal:
        # Criar DataFrame
        df_relatorio = pd.DataFrame(relatorio_semanal)

        # Formatar coluna de valor devido
        df_relatorio['Valor Devido'] = df_relatorio['valor_devido'].apply(utils.formatar_moeda)

        # Renomear colunas para exibição
        df_display = df_relatorio[[
            'nome', 'tipo', 'dias_trabalhados', 'total_entregas', 'Valor Devido'
        ]].rename(columns={
            'nome': 'Motoboy',
            'tipo': 'Tipo',
            'dias_trabalhados': 'Dias Trabalhados',
            'total_entregas': 'Total Entregas'
        })

        # Exibir tabela
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )

        # Gráficos
        col_graf1, col_graf2 = st.columns(2)

        with col_graf1:
            # Gráfico de entregas por motoboy
            fig_entregas = px.bar(
                df_relatorio,
                x='nome',
                y='total_entregas',
                color='tipo',
                title='Entregas por Motoboy (Semana)',
                labels={'nome': 'Motoboy', 'total_entregas': 'Entregas', 'tipo': 'Tipo'},
                color_discrete_map={'Fixo': '#1f77b4', 'Freelancer': '#ff7f0e'}
            )
            st.plotly_chart(fig_entregas, use_container_width=True)

        with col_graf2:
            # Gráfico de valores devidos
            df_fixos = df_relatorio[df_relatorio['tipo'] == 'Fixo']

            if not df_fixos.empty:
                fig_valores = px.bar(
                    df_fixos,
                    x='nome',
                    y='valor_devido',
                    title='Valores a Pagar - Motoboys Fixos (Semana)',
                    labels={'nome': 'Motoboy', 'valor_devido': 'Valor (R$)'},
                    color_discrete_sequence=['#2ca02c']
                )
                st.plotly_chart(fig_valores, use_container_width=True)
            else:
                st.info("Nenhum motoboy fixo com valores a pagar esta semana.")

        # Totalizadores
        total_geral_entregas = df_relatorio['total_entregas'].sum()
        total_geral_valor = df_relatorio['valor_devido'].sum()

        col_total1, col_total2, col_total3 = st.columns(3)

        with col_total1:
            st.metric("📦 Total Entregas (Semana)", total_geral_entregas)

        with col_total2:
            st.metric("💰 Total a Pagar (Semana)", utils.formatar_moeda(total_geral_valor))

        with col_total3:
            media_semanal = total_geral_entregas / len(df_relatorio) if len(df_relatorio) > 0 else 0
            st.metric("📊 Média Entregas/Motoboy (Semana)", f"{media_semanal:.1f}")

    else:
        st.info("ℹ️ Nenhum registro encontrado para esta semana.")

    st.divider()

    # SEÇÃO D: Assistente de IA
    st.subheader("🤖 Assistente de IA - Gemini 2.5 Flash")

    col_chat, col_sugestoes = st.columns([2, 1])

    with col_sugestoes:
        st.write("**💡 Perguntas Sugeridas:**")

        perguntas_sugeridas = ai_assistant.sugerir_perguntas()

        for pergunta in perguntas_sugeridas:
            if st.button(pergunta, key=f"sugestao_{pergunta[:20]}", use_container_width=True):
                # Adicionar pergunta ao chat
                st.session_state.chat_history.append({
                    "role": "user",
                    "message": pergunta
                })

                # Obter resposta da IA
                resposta = ai_assistant.get_gemini_response(
                    pergunta,
                    kpis_hoje,
                    relatorio_semanal,
                    config_atual
                )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "message": resposta
                })

                st.rerun()

    with col_chat:
        st.write("**💬 Chat com Assistente:**")

        # Container para o chat
        chat_container = st.container()

        with chat_container:
            # Exibir histórico de mensagens
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.chat_message("user").write(msg["message"])
                else:
                    st.chat_message("assistant").write(msg["message"])

        # Input do usuário
        user_input = st.chat_input("Digite sua pergunta sobre os dados...")

        if user_input:
            # Adicionar mensagem do usuário
            st.session_state.chat_history.append({
                "role": "user",
                "message": user_input
            })

            # Obter resposta da IA
            with st.spinner("🤔 Analisando dados..."):
                resposta = ai_assistant.get_gemini_response(
                    user_input,
                    kpis_hoje,
                    relatorio_semanal,
                    config_atual
                )

            st.session_state.chat_history.append({
                "role": "assistant",
                "message": resposta
            })

            st.rerun()

        # Botão para limpar chat
        if st.session_state.chat_history:
            if st.button("🗑️ Limpar Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()

# Rodapé
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🏍️ Sistema de Controle de Motoboys | Desenvolvido com Streamlit + Supabase + Gemini AI</p>
</div>
""", unsafe_allow_html=True)
