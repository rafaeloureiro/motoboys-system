"""
Utilitários para formatação de moeda e cálculos
"""
from datetime import datetime, timedelta
import locale

# Configurar locale para formato brasileiro
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        pass


def formatar_moeda(valor):
    """
    Formata valor para o padrão brasileiro R$ 1.234,56

    Args:
        valor: Valor numérico ou string

    Returns:
        String formatada no padrão brasileiro
    """
    try:
        if valor is None:
            return "R$ 0,00"

        # Converter para float se necessário
        if isinstance(valor, str):
            valor = float(valor.replace(',', '.'))

        valor = float(valor)

        # Formatar com separador de milhares e decimais
        valor_formatado = f"{valor:,.2f}"

        # Substituir vírgula por ponto temporariamente e vice-versa
        valor_formatado = valor_formatado.replace(',', 'X').replace('.', ',').replace('X', '.')

        return f"R$ {valor_formatado}"
    except:
        return "R$ 0,00"


def parse_moeda(valor_str):
    """
    Converte string no formato brasileiro para float

    Args:
        valor_str: String no formato "R$ 1.234,56" ou "1.234,56"

    Returns:
        Valor float
    """
    try:
        if valor_str is None or valor_str == "":
            return 0.0

        # Remover R$ e espaços
        valor_limpo = str(valor_str).replace('R$', '').strip()

        # Remover pontos de milhares e substituir vírgula por ponto
        valor_limpo = valor_limpo.replace('.', '').replace(',', '.')

        return float(valor_limpo)
    except:
        return 0.0


def calcular_custo_total(qtd_motoboys, total_entregas, valor_diaria, valor_corrida):
    """
    Calcula o custo total baseado na fórmula:
    (Quantidade de Motoboys * Valor Diária) + (Total de Entregas * Valor Corrida)

    Args:
        qtd_motoboys: Quantidade de motoboys
        total_entregas: Total de entregas realizadas
        valor_diaria: Valor da diária
        valor_corrida: Valor por corrida

    Returns:
        Custo total calculado
    """
    try:
        custo_diarias = qtd_motoboys * valor_diaria
        custo_corridas = total_entregas * valor_corrida
        return custo_diarias + custo_corridas
    except:
        return 0.0


def calcular_custo_medio_entrega(custo_total, total_entregas):
    """
    Calcula o custo médio por entrega

    Args:
        custo_total: Custo total
        total_entregas: Total de entregas

    Returns:
        Custo médio por entrega
    """
    try:
        if total_entregas == 0:
            return 0.0
        return custo_total / total_entregas
    except:
        return 0.0


def calcular_media_entregas_moto(total_entregas, qtd_motoboys):
    """
    Calcula a média de entregas por motoboy

    Args:
        total_entregas: Total de entregas
        qtd_motoboys: Quantidade de motoboys

    Returns:
        Média de entregas por motoboy
    """
    try:
        if qtd_motoboys == 0:
            return 0.0
        return total_entregas / qtd_motoboys
    except:
        return 0.0


def get_inicio_semana():
    """
    Retorna a data de início da semana (segunda-feira)

    Returns:
        Data da segunda-feira da semana atual
    """
    hoje = datetime.now()
    inicio_semana = hoje - timedelta(days=hoje.weekday())
    return inicio_semana.date()


def get_data_hoje():
    """
    Retorna a data de hoje

    Returns:
        Data de hoje
    """
    return datetime.now().date()


def formatar_data_br(data):
    """
    Formata data no padrão brasileiro DD/MM/YYYY

    Args:
        data: Data a ser formatada

    Returns:
        String formatada
    """
    try:
        if isinstance(data, str):
            data = datetime.strptime(data, '%Y-%m-%d').date()
        return data.strftime('%d/%m/%Y')
    except:
        return str(data)


def calcular_valor_devido_motoboy(registros, valor_diaria, valor_corrida):
    """
    Calcula o valor devido para um motoboy específico
    Regra: Fixo recebe diária + corridas; Freelancer já foi pago

    Args:
        registros: Lista de registros do motoboy
        valor_diaria: Valor da diária
        valor_corrida: Valor por corrida

    Returns:
        Valor total devido
    """
    try:
        valor_total = 0.0
        dias_trabalhados = set()
        total_entregas = 0

        for registro in registros:
            tipo = registro.get('tipo', 'Fixo')

            if tipo == 'Fixo':
                # Contar dias únicos para diária
                data = registro.get('data')
                if data:
                    dias_trabalhados.add(data)

                # Somar entregas para corridas
                entregas = registro.get('entregas', 0)
                total_entregas += entregas

        # Calcular valor devido apenas para fixos
        if len(registros) > 0 and registros[0].get('tipo') == 'Fixo':
            valor_total = (len(dias_trabalhados) * valor_diaria) + (total_entregas * valor_corrida)

        return valor_total
    except:
        return 0.0
