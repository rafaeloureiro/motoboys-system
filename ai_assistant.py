"""
Assistente de IA - Sistema Motoboys 2026
Correção Definitiva: SDK google-genai v1.56.0
"""
from google import genai
from google.genai import types
import streamlit as st
import utils

@st.cache_resource
def configurar_gemini():
    try:
        # Busca a chave conforme sua estrutura [google] -> api_key
        api_key = st.secrets["google"]["api_key"]
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Erro na API Key: {e}")
        return None

def preparar_contexto(kpis_hoje, relatorio_semanal, config):
    contexto = f"""
📊 DADOS DO SISTEMA

🔧 CONFIGURAÇÕES:
- Diária: {utils.formatar_moeda(config.get('valor_diaria', 0))}
- Corrida: {utils.formatar_moeda(config.get('valor_corrida', 0))}

📈 HOJE:
- Entregas: {kpis_hoje.get('total_entregas', 0)}
- Motoboys: {kpis_hoje.get('total_motoboys', 0)}
- Custo Total: {utils.formatar_moeda(kpis_hoje.get('custo_total', 0))}

📅 SEMANAL:
"""
    if relatorio_semanal:
        for m in relatorio_semanal:
            contexto += f"- {m['nome']}: {m['total_entregas']} ent. | {utils.formatar_moeda(m['valor_devido'])}\n"
    return contexto

def get_gemini_response(user_message, kpis_hoje, relatorio_semanal, config):
    try:
        client = configurar_gemini()
        if not client: return "❌ Erro de configuração."

        contexto = preparar_contexto(kpis_hoje, relatorio_semanal, config)

        # Na SDK 1.56.0+, use apenas o nome do modelo sem prefixos
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=f"Você é o Assistente Motoboy AI. Contexto: {contexto}",
                temperature=0.7,
            )
        )
        return response.text
    except Exception as e:
        # Se o erro 404 persistir, o problema é a ativação da API no console do Google
        return f"❌ Erro na API: {str(e)}"

def sugerir_perguntas():
    return ["Quem foi mais produtivo?", "Resumo de custos", "Dicas de economia"]
