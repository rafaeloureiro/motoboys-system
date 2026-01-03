"""
Gerenciamento de conexão e queries com Supabase
Otimizado para Supabase-py 2.x e Streamlit Cloud 2026
"""
import streamlit as st
from supabase import create_client, Client
from datetime import datetime, timedelta
import utils


@st.cache_resource
def get_supabase_client():
    """
    Cria e retorna cliente Supabase (cached para reutilização)

    Returns:
        Cliente Supabase configurado
    """
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro ao conectar com Supabase: {e}")
        return None


# ==================== REGISTROS ====================

def inserir_registro(nome, data, periodo, tipo, entregas):
    """
    Insere novo registro de motoboy

    Args:
        nome: Nome do motoboy
        data: Data do registro
        periodo: Manhã ou Noite
        tipo: Fixo ou Freelancer
        entregas: Número de entregas

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False

        data_obj = {
            "nome": nome,
            "data": str(data),
            "periodo": periodo,
            "tipo": tipo,
            "entregas": entregas,
            "created_at": datetime.now().isoformat()
        }

        response = supabase.table("registros").insert(data_obj).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir registro: {e}")
        return False


def buscar_registros_dia(data):
    """
    Busca todos os registros de uma data específica

    Args:
        data: Data para buscar registros

    Returns:
        Lista de registros
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []

        response = supabase.table("registros")\
            .select("*")\
            .eq("data", str(data))\
            .order("created_at", desc=True)\
            .execute()

        return response.data if response.data else []
    except Exception as e:
        st.error(f"Erro ao buscar registros do dia: {e}")
        return []


def buscar_registros_semana(data_inicio, data_fim):
    """
    Busca registros entre duas datas (semana)

    Args:
        data_inicio: Data de início
        data_fim: Data de fim

    Returns:
        Lista de registros
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []

        response = supabase.table("registros")\
            .select("*")\
            .gte("data", str(data_inicio))\
            .lte("data", str(data_fim))\
            .order("data", desc=False)\
            .execute()

        return response.data if response.data else []
    except Exception as e:
        st.error(f"Erro ao buscar registros da semana: {e}")
        return []


def atualizar_registro(registro_id, nome, data, periodo, tipo, entregas):
    """
    Atualiza registro existente

    Args:
        registro_id: ID do registro
        nome: Nome do motoboy
        data: Data do registro
        periodo: Manhã ou Noite
        tipo: Fixo ou Freelancer
        entregas: Número de entregas

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False

        data_obj = {
            "nome": nome,
            "data": str(data),
            "periodo": periodo,
            "tipo": tipo,
            "entregas": entregas
        }

        response = supabase.table("registros")\
            .update(data_obj)\
            .eq("id", registro_id)\
            .execute()

        return True
    except Exception as e:
        st.error(f"Erro ao atualizar registro: {e}")
        return False


def excluir_registro(registro_id):
    """
    Exclui registro

    Args:
        registro_id: ID do registro

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False

        response = supabase.table("registros")\
            .delete()\
            .eq("id", registro_id)\
            .execute()

        return True
    except Exception as e:
        st.error(f"Erro ao excluir registro: {e}")
        return False


# ==================== CONFIGURAÇÕES ====================

def buscar_configuracao_ativa():
    """
    Busca a configuração ativa mais recente

    Returns:
        Dicionário com valor_diaria e valor_corrida
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return {"valor_diaria": 0.0, "valor_corrida": 0.0}

        response = supabase.table("configuracoes")\
            .select("*")\
            .eq("ativa", True)\
            .order("created_at", desc=True)\
            .limit(1)\
            .execute()

        if response.data and len(response.data) > 0:
            config = response.data[0]
            return {
                "id": config.get("id"),
                "valor_diaria": config.get("valor_diaria", 0.0),
                "valor_corrida": config.get("valor_corrida", 0.0)
            }
        else:
            # Retornar valores padrão se não houver configuração
            return {"valor_diaria": 0.0, "valor_corrida": 0.0}
    except Exception as e:
        st.error(f"Erro ao buscar configuração ativa: {e}")
        return {"valor_diaria": 0.0, "valor_corrida": 0.0}


def salvar_configuracao(valor_diaria, valor_corrida):
    """
    Salva nova configuração e desativa as anteriores

    Args:
        valor_diaria: Valor da diária
        valor_corrida: Valor por corrida

    Returns:
        True se sucesso, False caso contrário
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return False

        # Desativar todas as configurações anteriores
        supabase.table("configuracoes")\
            .update({"ativa": False})\
            .eq("ativa", True)\
            .execute()

        # Inserir nova configuração ativa
        data_obj = {
            "valor_diaria": valor_diaria,
            "valor_corrida": valor_corrida,
            "ativa": True,
            "created_at": datetime.now().isoformat()
        }

        response = supabase.table("configuracoes").insert(data_obj).execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar configuração: {e}")
        return False


# ==================== ANÁLISES E RELATÓRIOS ====================

def calcular_kpis_dia(data):
    """
    Calcula KPIs do dia

    Args:
        data: Data para calcular KPIs

    Returns:
        Dicionário com KPIs
    """
    try:
        registros = buscar_registros_dia(data)
        config = buscar_configuracao_ativa()

        if not registros:
            return {
                "total_entregas": 0,
                "total_motoboys": 0,
                "media_entregas_moto": 0.0,
                "custo_total": 0.0,
                "custo_medio_entrega": 0.0
            }

        # Calcular métricas
        total_entregas = sum(r.get("entregas", 0) for r in registros)
        motoboys_unicos = len(set(r.get("nome") for r in registros))

        # Usar funções do utils para cálculos
        custo_total = utils.calcular_custo_total(
            motoboys_unicos,
            total_entregas,
            config.get("valor_diaria", 0.0),
            config.get("valor_corrida", 0.0)
        )

        custo_medio = utils.calcular_custo_medio_entrega(custo_total, total_entregas)
        media_entregas = utils.calcular_media_entregas_moto(total_entregas, motoboys_unicos)

        return {
            "total_entregas": total_entregas,
            "total_motoboys": motoboys_unicos,
            "media_entregas_moto": round(media_entregas, 2),
            "custo_total": custo_total,
            "custo_medio_entrega": round(custo_medio, 2)
        }
    except Exception as e:
        st.error(f"Erro ao calcular KPIs: {e}")
        return {
            "total_entregas": 0,
            "total_motoboys": 0,
            "media_entregas_moto": 0.0,
            "custo_total": 0.0,
            "custo_medio_entrega": 0.0
        }


def gerar_relatorio_semanal():
    """
    Gera relatório consolidado da semana (segunda até hoje)

    Returns:
        Lista de dicionários com dados consolidados por motoboy
    """
    try:
        data_inicio = utils.get_inicio_semana()
        data_hoje = utils.get_data_hoje()

        registros = buscar_registros_semana(data_inicio, data_hoje)
        config = buscar_configuracao_ativa()

        if not registros:
            return []

        # Agrupar por motoboy
        motoboys_dict = {}

        for registro in registros:
            nome = registro.get("nome")
            tipo = registro.get("tipo")
            entregas = registro.get("entregas", 0)
            data = registro.get("data")

            if nome not in motoboys_dict:
                motoboys_dict[nome] = {
                    "nome": nome,
                    "tipo": tipo,
                    "total_entregas": 0,
                    "dias_trabalhados": set(),
                    "registros": []
                }

            motoboys_dict[nome]["total_entregas"] += entregas
            motoboys_dict[nome]["dias_trabalhados"].add(data)
            motoboys_dict[nome]["registros"].append(registro)

        # Calcular valores devidos
        relatorio = []
        for nome, dados in motoboys_dict.items():
            dias_trab = len(dados["dias_trabalhados"])
            total_entregas = dados["total_entregas"]
            tipo = dados["tipo"]

            # Calcular valor devido
            if tipo == "Fixo":
                valor_devido = (
                    dias_trab * config.get("valor_diaria", 0.0) +
                    total_entregas * config.get("valor_corrida", 0.0)
                )
            else:  # Freelancer
                valor_devido = 0.0  # Já foi pago no dia

            relatorio.append({
                "nome": nome,
                "tipo": tipo,
                "dias_trabalhados": dias_trab,
                "total_entregas": total_entregas,
                "valor_devido": valor_devido
            })

        # Ordenar por nome
        relatorio.sort(key=lambda x: x["nome"])

        return relatorio
    except Exception as e:
        st.error(f"Erro ao gerar relatório semanal: {e}")
        return []


def buscar_nomes_motoboys():
    """
    Busca lista única de nomes de motoboys para autocomplete

    Returns:
        Lista de nomes únicos
    """
    try:
        supabase = get_supabase_client()
        if not supabase:
            return []

        response = supabase.table("registros")\
            .select("nome")\
            .execute()

        if response.data:
            nomes = list(set(r.get("nome") for r in response.data if r.get("nome")))
            nomes.sort()
            return nomes
        return []
    except Exception as e:
        st.error(f"Erro ao buscar nomes de motoboys: {e}")
        return []
