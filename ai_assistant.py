"""
Assistente de IA integrado com Google Gemini 2.5 Flash
Otimizado para Streamlit Cloud 2026
Usando a nova biblioteca google.genai
"""
from google import genai
from google.genai import types
import streamlit as st
import utils


@st.cache_resource
def configurar_gemini():
    """
    Configura o cliente Gemini com a API key (cached)

    Returns:
        Cliente Gemini configurado
    """
    try:
        api_key = st.secrets["google"]["api_key"]
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Erro ao configurar Gemini: {e}")
        return None


def preparar_contexto(kpis_hoje, relatorio_semanal, config):
    """
    Prepara o contexto com dados do sistema para o assistente

    Args:
        kpis_hoje: Dicionário com KPIs do dia
        relatorio_semanal: Lista com dados consolidados da semana
        config: Configurações atuais (valor_diaria, valor_corrida)

    Returns:
        String formatada com o contexto
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

    Args:
        user_message: Mensagem do usuário
        kpis_hoje: KPIs do dia atual
        relatorio_semanal: Dados consolidados da semana
        config: Configurações atuais

    Returns:
        Resposta do assistente
    """
    try:
        client = configurar_gemini()
        if not client:
            return "❌ Erro ao conectar com o assistente de IA. Verifique a API key do Google Gemini."

        # Preparar contexto com dados reais
        contexto = preparar_contexto(kpis_hoje, relatorio_semanal, config)

        # Prompt do sistema
        system_instruction = f"""
Você é um assistente especializado em logística e gestão de entregas. Seu nome é "Assistente Motoboy AI".

CONTEXTO DO SISTEMA:
{contexto}

INSTRUÇÕES:
1. Use SEMPRE os dados reais fornecidos acima para responder
2. Seja direto e objetivo nas respostas
3. Use português brasileiro
4. Formate valores monetários no padrão R$ 1.234,56
5. Sugira melhorias de eficiência quando apropriado
6. Identifique padrões e anomalias nos dados
7. Ajude com análises de custo-benefício
8. Proponha otimizações operacionais

TIPOS DE ANÁLISES QUE VOCÊ PODE FAZER:
- Análise de produtividade por motoboy
- Comparação entre motoboys fixos e freelancers
- Identificação de custos altos
- Sugestões de economia
- Previsões e tendências
- Avaliação de eficiência operacional

Responda de forma profissional, mas acessível. Use emojis ocasionalmente para facilitar a leitura.
"""

        # Gerar resposta usando a nova API
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
        return f"❌ Erro ao processar sua pergunta: {str(e)}\n\nVerifique se a API key do Google Gemini está configurada corretamente no arquivo .streamlit/secrets.toml"


def sugerir_perguntas():
    """
    Retorna lista de perguntas sugeridas para o usuário

    Returns:
        Lista de strings com perguntas sugeridas
    """
    return [
        "Qual motoboy foi mais produtivo esta semana?",
        "Como posso reduzir os custos operacionais?",
        "Vale mais a pena contratar fixo ou freelancer?",
        "Qual é a média de entregas por motoboy hoje?",
        "Existem motoboys com baixa produtividade?",
        "Quanto estou gastando por entrega em média?",
        "Como está o desempenho desta semana comparado ao normal?",
        "Quais insights você pode me dar sobre os dados de hoje?"
    ]
