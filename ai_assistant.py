"""
Assistente de IA para o Sistema de Motoboys
Versão 2026 - Otimizada para Google GenAI SDK
Modelo: Gemini 1.5 Flash (Estável e Gratuito)
"""
import streamlit as st
from google import genai

def get_gemini_response(pergunta, kpis_hoje, relatorio_semanal, config_atual):
    """
    Consulta o Gemini 1.5 Flash para análise de dados logísticos.
    Utiliza a nova SDK 'google-genai' conforme logs de dependências.
    """
    try:
        # 1. Configuração do Cliente
        # A chave deve estar em .streamlit/secrets.toml ou no painel do Streamlit Cloud
        api_key = st.secrets["google"]["api_key"]
        client = genai.Client(api_key=api_key)

        # 2. Preparação do Contexto (Data-Driven Prompt)
        # Transformamos os dados do banco em texto para a IA processar
        contexto_dados = f"""
        Você é o 'Assistente Motoboy AI', um analista especializado em logística de delivery.
        
        CONTEXTO OPERACIONAL ATUAL:
        - Valor da Diária: {config_atual.get('valor_diaria', 0)}
        - Valor por Corrida: {config_atual.get('valor_corrida', 0)}
        
        DADOS DE HOJE:
        - Total de Entregas: {kpis_hoje.get('total_entregas')}
        - Motoboys Ativos: {kpis_hoje.get('total_motoboys')}
        - Custo Total: {kpis_hoje.get('custo_total')}
        - Custo Médio por Entrega: {kpis_hoje.get('custo_medio_entrega')}
        
        DADOS SEMANAIS:
        {relatorio_semanal}

        INSTRUÇÕES:
        - Seja conciso e direto ao ponto.
        - Se o usuário perguntar sobre custos, sugira formas de otimizar a média por entrega.
        - Se perguntar sobre produtividade, cite o motoboy com mais entregas.
        - Use emojis de moto 🏍️ e entregas 📦 ocasionalmente.
        """

        # 3. Chamada da API
        # Alterado para 'gemini-1.5-flash-002' para evitar o erro 404
        response = client.models.generate_content(
            model='gemini-1.5-flash-002',
            contents=f"{contexto_dados}\n\nPERGUNTA DO USUÁRIO: {pergunta}"
        )

        return response.text

    except Exception as e:
        # Captura erros de cota (429) ou autenticação
        if "429" in str(e):
            return "⚠️ Limite de mensagens gratuitas atingido por este minuto. Tente novamente em instantes."
        return f"❌ Erro na IA: {str(e)}"

def sugerir_perguntas():
    """
    Retorna uma lista de perguntas frequentes para facilitar o uso pelo gestor.
    """
    return [
        "Qual o resumo financeiro de hoje?",
        "Quem é o motoboy mais produtivo da semana?",
        "Como reduzir o custo médio por entrega?",
        "Resumo das entregas de hoje"
    ]
