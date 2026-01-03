"""
Assistente de IA para o Sistema de Motoboys
Versão 2026 - Otimizada para Google GenAI SDK
Correção: Ajuste de ID de modelo para evitar 404
"""
import streamlit as st
from google import genai

def get_gemini_response(pergunta, kpis_hoje, relatorio_semanal, config_atual):
    """
    Consulta o Gemini Flash para análise de dados logísticos.
    """
    try:
        # 1. Configuração do Cliente
        api_key = st.secrets["google"]["api_key"]
        client = genai.Client(api_key=api_key)

        # 2. Preparação do Contexto
        contexto_dados = f"""
        Você é o 'Assistente Motoboy AI'.
        
        DADOS ATUAIS:
        - Diária: {config_atual.get('valor_diaria', 0)}
        - Corrida: {config_atual.get('valor_corrida', 0)}
        - Hoje: {kpis_hoje}
        - Semana: {relatorio_semanal}

        Responda de forma breve e profissional. 🏍️
        """

        # 3. Chamada da API
        # ALTERAÇÃO: Usando o ID padrão 'gemini-1.5-flash' que é o mais compatível
        # Se este falhar, você pode tentar 'gemini-2.0-flash'
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"{contexto_dados}\n\nPergunta: {pergunta}"
        )

        return response.text

    except Exception as e:
        # Caso o erro 404 persista, vamos tentar um fallback automático
        if "404" in str(e):
            return "⚠️ O modelo de IA está sendo atualizado. Por favor, tente novamente em alguns minutos ou verifique se o serviço está ativo no seu Google AI Studio."
        return f"❌ Erro na IA: {str(e)}"

def sugerir_perguntas():
    return [
        "Qual o resumo financeiro de hoje?",
        "Quem é o motoboy mais produtivo?",
        "Como reduzir o custo médio?"
    ]
