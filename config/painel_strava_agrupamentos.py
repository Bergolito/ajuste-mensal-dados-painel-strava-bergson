# =======================================================
# Imports
# =======================================================
import pandas as pd

from painel_strava_funcoes import *

# =======================================================
# Datasets
# =======================================================
df_atividades_todos = pd.read_csv('datasets/predados/atividades_fisicas_todos.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2020 = pd.read_csv('datasets/predados/atividades_fisicas_2020.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2021 = pd.read_csv('datasets/predados/atividades_fisicas_2021.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2022 = pd.read_csv('datasets/predados/atividades_fisicas_2022.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2023 = pd.read_csv('datasets/predados/atividades_fisicas_2023.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2024 = pd.read_csv('datasets/predados/atividades_fisicas_2024.csv', sep=',', encoding="ISO-8859-1")
df_atividades_completo_2025 = pd.read_csv('datasets/predados/atividades_fisicas_2025.csv', sep=',', encoding="ISO-8859-1")

df_atividades_simplificado_todos = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_todos.csv', sep=',', encoding="ISO-8859-1")
df_atividades_simplificado_2020 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2020.csv', sep=',', encoding="ISO-8859-1")
df_atividades_simplificado_2021 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2021.csv', sep=',', encoding="ISO-8859-1")
df_atividades_simplificado_2022 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2022.csv', sep=',', encoding="ISO-8859-1")
df_atividades_simplificado_2023 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2023.csv', sep=',', encoding="ISO-8859-1")
df_atividades_simplificado_2024 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2024.csv', sep=',', encoding="UTF-8")
df_atividades_simplificado_2025 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2025.csv', sep=',', encoding="ISO-8859-1")

# =======================================================
# Funções
# =======================================================

# =======================================================
def agrupamento_atividade_por_tipo_por_ano(df, ano):
  df_filtrado = retorna_atividades_ano(df, ano)
  contagem_por_tipo = df_filtrado['Activity Type'].value_counts().reset_index()
  contagem_por_tipo.columns = ['tipo_atividade', 'qtd']
  contagem_por_tipo['ano'] = ano

  return contagem_por_tipo
# =======================================================
def agrupamento_atividade_por_tipo_por_ano_mes(df, ano, mes):
  df_filtrado = retorna_atividades_mes_ano(df, ano, mes)
  contagem_por_tipo = df_filtrado['Activity Type'].value_counts().reset_index()
  contagem_por_tipo.columns = ['tipo_atividade', 'qtd']
  contagem_por_tipo['ano'] = ano
  contagem_por_tipo['mes'] = mes

  return contagem_por_tipo
# =======================================================
def agrupamento_atividade_por_diasemana_por_ano(df, ano):
  df_filtrado = retorna_atividades_ano(df, ano)
  contagem_por_dia_semana = df_filtrado['dia_semana'].value_counts().reset_index()
  contagem_por_dia_semana.columns = ['dia_semana', 'qtd']
  contagem_por_dia_semana['ano'] = ano

  return contagem_por_dia_semana
# =======================================================
def agrupamento_atividade_por_diasemana_por_ano_mes(df, ano, mes):
  df_filtrado = retorna_atividades_mes_ano(df, ano, mes)
  contagem_por_dia_semana = df_filtrado['dia_semana'].value_counts().reset_index()
  contagem_por_dia_semana.columns = ['dia_semana', 'qtd']
  contagem_por_dia_semana['ano'] = ano
  contagem_por_dia_semana['mes'] = mes

  return contagem_por_dia_semana
# =======================================================

# =======================================================
def processa_atividades_geral_tipo_ano():

    contagem_por_tipo_2020 = agrupamento_atividade_por_tipo_por_ano(df_atividades_simplificado_2020, 2020)
    contagem_por_tipo_2021 = agrupamento_atividade_por_tipo_por_ano(df_atividades_simplificado_2021, 2021)
    contagem_por_tipo_2022 = agrupamento_atividade_por_tipo_por_ano(df_atividades_simplificado_2022, 2022)
    contagem_por_tipo_2023 = agrupamento_atividade_por_tipo_por_ano(df_atividades_simplificado_2023, 2023)
    contagem_por_tipo_2024 = agrupamento_atividade_por_tipo_por_ano(df_atividades_simplificado_2024, 2024)
    contagem_por_tipo_2025 = agrupamento_atividade_por_tipo_por_ano(df_atividades_simplificado_2025, 2025)
    
    atvs_por_tipo_concatenados = pd.concat(
    [
        contagem_por_tipo_2020, contagem_por_tipo_2021, contagem_por_tipo_2022, 
        contagem_por_tipo_2023, contagem_por_tipo_2024, contagem_por_tipo_2025
    
    ], axis=0)
    
    atvs_por_tipo_concatenados
    
    df_tipo = atvs_por_tipo_concatenados
    df_geral_tipo = pd.DataFrame(columns=['tipo_atividade','qtd','ano'])

    lista_atividades = contagem_por_tipo_2024['tipo_atividade'].unique()
    
    for item in lista_atividades:
      df_filtrado_tipo = df_tipo[(df_tipo['tipo_atividade'] == item)]
      df_geral_tipo = pd.concat([df_geral_tipo, df_filtrado_tipo], ignore_index=True)
    
    df_geral_tipo.to_csv('datasets/gerais/atividades_geral_por_tipo.csv', index=False)
    print('\n\nSalvando arquivo atividades_geral_por_tipo.csv...')
    
    return df_geral_tipo
# =======================================================
def processa_atividades_geral_tipo_ano_mes():

    lista_dfs_ano = [
       (df_atividades_simplificado_2020, 2020),
       (df_atividades_simplificado_2021, 2021),
       (df_atividades_simplificado_2022, 2022),
       (df_atividades_simplificado_2023, 2023),
       (df_atividades_simplificado_2024, 2024),
       (df_atividades_simplificado_2025, 2025),
    ]

    lista_de_dfs = []
    for item in lista_dfs_ano:
      df = item[0]
      ano = item[1]
      for mes in range(1,13):
        df_ano_mes = agrupamento_atividade_por_tipo_por_ano_mes(df, ano, mes)
        lista_de_dfs.append(df_ano_mes)

    # Concatenando os DataFrames verticalmente
    atvs_por_tipo_concatenados = pd.concat(lista_de_dfs)

    atvs_por_tipo_concatenados
    
    df_tipo = atvs_por_tipo_concatenados
    df_geral_tipo = pd.DataFrame(columns=['tipo_atividade','qtd','ano','mes'])

    lista_atividades = df_tipo['tipo_atividade'].unique()
    
    for item in lista_atividades:
      df_filtrado_tipo = df_tipo[(df_tipo['tipo_atividade'] == item)]
      df_geral_tipo = pd.concat([df_geral_tipo, df_filtrado_tipo], ignore_index=True)
    
    df_geral_tipo.to_csv('datasets/gerais/atividades_geral_por_tipo_ano_mes.csv', index=False)
    print('\n\nSalvando arquivo atividades_geral_por_tipo_ano_mes.csv...')
    
    return df_geral_tipo
# =======================================================
def processa_atividades_geral_dia_semana_ano():

    contagem_por_tipo_2020 = agrupamento_atividade_por_diasemana_por_ano(df_atividades_simplificado_2020, 2020)
    contagem_por_tipo_2021 = agrupamento_atividade_por_diasemana_por_ano(df_atividades_simplificado_2021, 2021)
    contagem_por_tipo_2022 = agrupamento_atividade_por_diasemana_por_ano(df_atividades_simplificado_2022, 2022)
    contagem_por_tipo_2023 = agrupamento_atividade_por_diasemana_por_ano(df_atividades_simplificado_2023, 2023)
    contagem_por_tipo_2024 = agrupamento_atividade_por_diasemana_por_ano(df_atividades_simplificado_2024, 2024)
    contagem_por_tipo_2025 = agrupamento_atividade_por_diasemana_por_ano(df_atividades_simplificado_2025, 2025)
    
    atvs_por_tipo_concatenados = pd.concat(
    [
        contagem_por_tipo_2020, contagem_por_tipo_2021, contagem_por_tipo_2022, 
        contagem_por_tipo_2023, contagem_por_tipo_2024, contagem_por_tipo_2025
    
    ], axis=0)
    
    atvs_por_tipo_concatenados
    
    df_tipo = atvs_por_tipo_concatenados
    df_geral_tipo = pd.DataFrame(columns=['dia_semana','qtd','ano'])

    lista_atividades = contagem_por_tipo_2024['dia_semana'].unique()
    
    for item in lista_atividades:
      df_filtrado_tipo = df_tipo[(df_tipo['dia_semana'] == item)]
      df_geral_tipo = pd.concat([df_geral_tipo, df_filtrado_tipo], ignore_index=True)
    
    df_geral_tipo.to_csv('datasets/gerais/atividades_geral_por_dia_semana.csv', index=False)
    print('\n\nSalvando arquivo atividades_geral_por_dia_semana.csv...')
    
    return df_geral_tipo
# =======================================================
def processa_atividades_geral_dia_semana_ano_mes():

    lista_dfs_ano = [
       (df_atividades_simplificado_2020, 2020),
       (df_atividades_simplificado_2021, 2021),
       (df_atividades_simplificado_2022, 2022),
       (df_atividades_simplificado_2023, 2023),
       (df_atividades_simplificado_2024, 2024),
       (df_atividades_simplificado_2025, 2025),
    ]

    lista_de_dfs = []
    for item in lista_dfs_ano:
      df = item[0]
      ano = item[1]
      for mes in range(1,13):
        df_ano_mes = agrupamento_atividade_por_diasemana_por_ano_mes(df, ano, mes)
        lista_de_dfs.append(df_ano_mes)

    # Concatenando os DataFrames verticalmente
    atvs_por_tipo_concatenados = pd.concat(lista_de_dfs)

    atvs_por_tipo_concatenados
    
    df_tipo = atvs_por_tipo_concatenados
    df_geral_tipo = pd.DataFrame(columns=['dia_semana','qtd','ano','mes'])

    lista_atividades = df_tipo['dia_semana'].unique()
    
    for item in lista_atividades:
      df_filtrado_tipo = df_tipo[(df_tipo['dia_semana'] == item)]
      df_geral_tipo = pd.concat([df_geral_tipo, df_filtrado_tipo], ignore_index=True)
    
    df_geral_tipo.to_csv('datasets/gerais/atividades_geral_por_dia_semana_ano_mes.csv', index=False)
    print('\n\nSalvando arquivo atividades_geral_por_dia_semana_ano_mes.csv...')
    
    return df_geral_tipo
# =======================================================
