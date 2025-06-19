# =======================================================
# Imports
# =======================================================
import pandas as pd

from painel_strava_agrupamentos import *

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
def gera_dados_gerais():

  # gera dados dos tipos de atividades
  gera_dados_gerais_tipo_atividades()

  # gera dados dos dias da semana 
  gera_dados_gerais_dia_semana_atividades()

  gera_sumarios_anos()
# =======================================================
def gera_dados_gerais_tipo_atividades():

  processa_atividades_geral_tipo_ano()
  processa_atividades_geral_tipo_ano_mes()
  processa_atividades_geral_tipo_ano_mes()

# =======================================================
def gera_dados_gerais_dia_semana_atividades():

  processa_atividades_geral_dia_semana_ano()
  processa_atividades_geral_dia_semana_ano_mes()
# =======================================================
def gera_sumario_atividades_por_ano(df, ano):

  df_sumario = pd.DataFrame(columns=['ano','mes','qtd','distancia','calorias'])
  df_sumario_geral = pd.DataFrame(columns=['ano','mes','qtd','distancia','calorias'])
  
  for mes in range(1,13):
    df_filtrado = retorna_atividades_mes_ano(df, ano, mes)
    print(f'ano {ano} | mes {mes} | {df_filtrado.shape[0]}')
    qtd = df_filtrado.shape[0]
    distancia = df_filtrado['Distance'].sum()
    calorias = df_filtrado['Calories'].sum()
    print(f'qtd => {qtd} | distancia =>  {distancia} | calorias => {calorias}')

    df_sumario.loc[0,'ano'] = ano
    df_sumario.loc[0,'mes'] = mes
    df_sumario.loc[0,'qtd'] = qtd
    df_sumario.loc[0,'distancia'] = distancia
    df_sumario.loc[0,'calorias'] = calorias

    print(f'df_sumario => {df_sumario.shape}')
    df_sumario_geral = pd.concat([df_sumario_geral, df_sumario], ignore_index=True)

  print(f'df_sumario_geral => {df_sumario_geral.shape[0]}')

  return df_sumario_geral
# =======================================================

def gera_sumarios_anos():

  lista_dfs_ano = [
      (df_atividades_simplificado_2020, 2020),
      (df_atividades_simplificado_2021, 2021),
      (df_atividades_simplificado_2022, 2022),
      (df_atividades_simplificado_2023, 2023),
      (df_atividades_simplificado_2024, 2024),
      (df_atividades_simplificado_2025, 2025),
  ]

  for item in lista_dfs_ano:
    print(f'item[0] => {item[0].shape[0]} | item[1] => {item[1]}')
    df_sumario_ano = gera_sumario_atividades_por_ano(item[0], item[1])
    df_sumario_ano.to_csv(f'datasets/gerais/sumario_atividades_{item[1]}.csv')
    print(f'\n\nSalvando arquivo datasets/gerais/sumario_atividades_{item[1]}.csv...')
  
# =======================================================
# main 
# =======================================================



# ==================================
if __name__ == "__main__":
  # Executa o código
  gera_dados_gerais()
# ==================================  
