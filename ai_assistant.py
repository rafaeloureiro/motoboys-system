"""
Assistente de IA integrado com Google Gemini 1.5 Flash
Otimizado para Streamlit Cloud
Usando a nova biblioteca google.genai (SDK v2)
"""
from google import genai
from google.genai import types
import streamlit as st
import utils


@st.cache_resource
def configurar_gemini():
    """
    Configura o cliente Gemini com a API key (cached)
    """
    try:
        # IMPORTANTE: O arquivo secrets.toml deve ter a seção [google]
        api_key = st.secrets["google"]["api_key"]
        
        # Na nova SDK google-genai, a configuração é via Client
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Erro de configuração: {e}")
        return None


def preparar_contexto(kpis_hoje, relatorio_semanal, config):
    """
    Prepara o contexto com dados do sistema para o assistente
    """
    contexto = f"""
📊 DADOS DO SISTEMA - CONTROLE DE MOTOBOYS

🔧 CONFIGURAÇÕES ATUAIS:
- Valor da Diária: {utils.formatar_moeda(config.get('valor_diaria', 0))}
- Valor por Corrida: {utils.formatar_moeda(config.get('valor_corrida', 0))}

📈 KPIs DE HOJE:
- Total de Entregas: {kpis_hoje.get('total_entregas', 0)}
- Total de Motoboys: {kpis_hoje.get('total_motoboys', 0)}
- Média Entregas/Motoboy: {kpis_hoje.get('media_entregas_moto', 0):.2f}
- Custo Total: {utils.formatar_moeda(kpis_hoje.get('custo_total', 0))}
- Custo Médio por Entrega: {utils.formatar_moeda(kpis_hoje.get('custo_medio_entrega', 0))}

📅 RESUMO SEMANAL (Segunda até Hoje):
"""

    if relatorio_semanal:
        for motoboy in relatorio_semanal:
            tipo_emoji = "🔧" if motoboy['tipo'] == "Fixo" else "🏍️"
            contexto += f"""
{tipo_emoji} {motoboy['nome']} ({motoboy['tipo']}):
   - Dias Trabalhados: {motoboy['dias_trabalhados']}
   - Total Entregas: {motoboy['total_entregas']}
   - Valor Devido: {utils.formatar_moeda(motoboy['valor_devido'])}
"""
    else:
        contexto += "\n(Nenhum registro esta semana)\n"

    return contexto


def get_gemini_response(user_message, kpis_hoje, relatorio_semanal, config):
    """
    Obtém resposta do Gemini com contexto do sistema
    """
    try:
        client = configurar_gemini()
        if not client:
            return "❌ Erro: Cliente Gemini não configurado."

        # Preparar contexto
        contexto = preparar_contexto(kpis_hoje, relatorio_semanal, config)

        # Instrução do Sistema
        system_instruction = f"""
Você é o "Assistente Motoboy AI".
CONTEXTO: {contexto}
INSTRUÇÕES: Seja direto, use R$ para valores e baseie-se apenas nos dados acima.
"""

        # CORREÇÃO DEFINITIVA: 
        # Algumas versões da SDK v2 preferem o nome direto do modelo.
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )

        return response.text

    except Exception as e:
        # Se o erro 404 persistir, ele será capturado aqui com detalhes
        return f"❌ Erro ao processar sua pergunta: {str(e)}"


def sugerir_perguntas():
    return [
        "Qual motoboy foi mais produtivo esta semana?",
        "Como posso reduzir os custos operacionais?",
        "Qual é a média de entregas por motoboy hoje?",
        "Quais insights você pode me dar sobre os dados de hoje?"
    ]
