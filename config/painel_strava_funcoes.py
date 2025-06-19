# =======================================================
# Imports
# =======================================================
from datetime import datetime

# ==================================
# Funções
# ==================================

# ==================================
def calcula_tempo_atv_minutos(tempo):
    return (tempo / 60)
# ==================================
def retorna_ano_data(data_string):
    formato = "%b %d, %Y, %I:%M:%S %p"  # Formato da sua string de data
    data_objeto = datetime.strptime(data_string, formato)
    ano = data_objeto.year

    return ano
# ==================================
def retorna_mes_data(data_string):
    formato = "%b %d, %Y, %I:%M:%S %p"  # Formato da sua string de data
    data_objeto = datetime.strptime(data_string, formato)
    mes = data_objeto.month

    return mes
# ==================================
def retorna_dia_semana_data(data_string):
    formato = "%b %d, %Y, %I:%M:%S %p"  # Formato da sua string de data
    data_objeto = datetime.strptime(data_string, formato)
    dia_semana = data_objeto.day

    return dia_semana
# ==================================
def retorna_dia_da_semana(data_string):
    """
    Recebe uma string de data no formato "Jan 6, 2025, 11:12:46 PM"
    e retorna o dia da semana.
    """
    try:
        data = datetime.strptime(data_string, "%b %d, %Y, %I:%M:%S %p")

        dias_da_semana = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
        dia_da_semana_numero = data.weekday()
        return dias_da_semana[dia_da_semana_numero]
    except ValueError:
        return "Formato de data inválido. Use 'Jan 6, 2025, 11:12:46 PM'."

# ==================================
def retorna_atividades_mes_ano(df2, ano, mes):
    df_lista_mes_ano = df2[(df2['data_ano'] == int(ano)) & (df2['data_mes'] == int(mes)) ]
    return df_lista_mes_ano    
# ==================================
def retorna_atividades_ano_por_mes(df2, ano):
    lista_dfs_mes = []

    for mes in range(1,13):
        df_lista_mes = df2[(df2['data_ano'] == int(ano)) & (df2['data_mes'] == int(mes)) ]
        lista_dfs_mes.append(df_lista_mes)

    return lista_dfs_mes    
# ==================================
def obter_mes_por_numero(numero):
  """
  Retorna o nome do mês correspondente ao número fornecido.

  Args:
    numero: Um número inteiro entre 0 e 11, representando um mês (0 = Janeiro, 1 = Fevereiro, ..., 11 = Dezembro).

  Returns:
    O nome do mês correspondente ao número fornecido, ou None se o número for inválido.
  """

  meses = [
      "Janeiro", "Fevereiro", "Março", "Abril",
      "Maio", "Junho", "Julho", "Agosto",
      "Setembro", "Outubro", "Novembro", "Dezembro"
  ]

  if 1 <= numero <= 12:
    return meses[numero-1]
  else:
    return None  # Número inválido
# ==================================
def retorna_atividades_ano(df2, ano):

    df_lista_ano = df2[(df2['data_ano'] == int(ano)) ]

    return df_lista_ano    
# ==================================
def retorna_atividades_df_por_mes(df2):
    lista_dfs_mes = []

    for mes in range(1,13):
        df_lista_mes = df2[(df2['data_mes'] == int(mes)) ]
        lista_dfs_mes.append(df_lista_mes)

    return lista_dfs_mes    
# ==================================
