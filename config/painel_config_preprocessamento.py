# =======================================================
# Imports
# =======================================================
import pandas as pd
import zipfile
import os

from datetime import datetime
from painel_strava_funcoes import *

# ==================================
# Funções
# ==================================

# ==================================
def salvar_arquivos_atividades_completos_anos():
  df_atividades_todos = pd.read_csv('datasets/atividades.csv', sep=',', encoding="ISO-8859-1")

  df2 = df_atividades_todos.copy()
  df2['data_ano'] = df_atividades_todos['Activity Date'].apply(retorna_ano_data)
  df2['data_mes'] = df_atividades_todos['Activity Date'].apply(retorna_mes_data)
  df2['dia_semana'] = df_atividades_todos['Activity Date'].apply(retorna_dia_da_semana)
  df2['tempo_min'] = df_atividades_todos['Elapsed Time'].apply(calcula_tempo_atv_minutos)

  lista_anos = df2['data_ano'].unique()
  print(f'Lista de anos = {lista_anos}')

  lista_colunas_dropar_01 = [
      "Total Work","Number of Runs","Uphill Time","Downhill Time","Other Time","Perceived Exertion","Type","Start Time","Weighted Average Power","Power Count",
      "Prefer Perceived Exertion","Perceived Relative Effort"
  ]
  lista_colunas_dropar_02 = [
      "Weather Observation Time","Weather Condition","Weather Temperature","Apparent Temperature","Dewpoint","Humidity","Weather Pressure",
      "Wind Speed","Wind Gust","Wind Bearing","Precipitation Intensity","Sunrise Time","Sunset Time",	
      "Moon Phase","Bike","Gear","Precipitation Probability","Precipitation Type","Cloud Cover","Weather Visibility",
      "UV Index","Weather Ozone","Jump Count","Total Grit","Average Flow","Flagged","Average Elapsed Speed","Dirt Distance",	
      "Newly Explored Distance","Newly Explored Dirt Distance","Activity Count","Total Steps","Carbon Saved","Pool Length","Training Load",
      "Intensity","Average Grade Adjusted Pace","Timer Time","Total Cycles","Media"
  ]

  df2.drop(lista_colunas_dropar_01, axis=1, inplace=True)
  df2.drop(lista_colunas_dropar_02, axis=1, inplace=True)

  nome_arquivo = f'datasets/predados/atividades_fisicas_todos.csv'
  print(f'Gerado arquivo de atvs fisicas => {nome_arquivo}...')
  df2.to_csv(nome_arquivo)

  for ano in lista_anos:
    df_atvs_ano = retorna_atividades_ano(df2, ano)
    nome_arquivo = f'datasets/predados/atividades_fisicas_{ano}.csv'
    print(f'Gerado arquivo de atvs fisicas => {nome_arquivo}...')
    df_atvs_ano.to_csv(nome_arquivo)
# ==================================
def salvar_arquivos_atividades_simplificados_anos():
  
  lista_dfs_anos = []
  df_atividades_2020 = pd.read_csv('datasets/predados/atividades_fisicas_2020.csv', sep=',', encoding="ISO-8859-1")
  df_atividades_2021 = pd.read_csv('datasets/predados/atividades_fisicas_2021.csv', sep=',', encoding="ISO-8859-1")
  df_atividades_2022 = pd.read_csv('datasets/predados/atividades_fisicas_2022.csv', sep=',', encoding="ISO-8859-1")
  df_atividades_2023 = pd.read_csv('datasets/predados/atividades_fisicas_2023.csv', sep=',', encoding="ISO-8859-1")
  df_atividades_2024 = pd.read_csv('datasets/predados/atividades_fisicas_2024.csv', sep=',', encoding="ISO-8859-1")
  df_atividades_2025 = pd.read_csv('datasets/predados/atividades_fisicas_2025.csv', sep=',', encoding="ISO-8859-1")
  df_atividades_todos = pd.read_csv('datasets/predados/atividades_fisicas_todos.csv', sep=',', encoding="ISO-8859-1")

  lista_dfs_anos = [
    (2020,df_atividades_2020),
    (2021,df_atividades_2021),
    (2022,df_atividades_2022),
    (2023,df_atividades_2023),
    (2024,df_atividades_2024),
    (2025,df_atividades_2025)
  ] 

  nome_arquivo = f'datasets/predados/atividades_fisicas_simplificado_todos.csv'
  print(f'Gerado arquivo de atvs fisicas => {nome_arquivo}...')
  lista_colunas_dropar_03 = [
    'Relative Effort',	'Commute',	'Activity Private Note',	'Activity Gear',	
    #'Filename',	É necessário para recuperar os arquivos das rotas
    'Athlete Weight',	'Bike Weight',	
    'Elapsed Time.1',	
    'Moving Time',	'Distance.1',	'Elevation Gain',	'Elevation Loss',	'Elevation Low',	'Elevation High',	'Max Grade',	
    'Average Grade',	
    'Average Positive Grade',	'Average Negative Grade',	'Max Cadence',	'Average Cadence',	'Max Heart Rate.1',	
    'Average Heart Rate',	'Max Watts',	'Average Watts',
    'Max Temperature',	'Average Temperature',	'Relative Effort.1',	'Commute.1',	'Total Weight Lifted',	'From Upload',	'Grade Adjusted Distance'
  ]

  df_atividades_todos.drop(lista_colunas_dropar_03, axis=1, inplace=True)
  df_atividades_todos.to_csv(nome_arquivo)

  for item in lista_dfs_anos:
    ano = item[0]
    df_atividades_ano = item[1]
    # Supondo que seu DataFrame seja chamado 'df'
    df_atvs_ano = retorna_atividades_ano(df_atividades_ano, ano)
    nome_arquivo = f'datasets/predados/atividades_fisicas_simplificado_{ano}.csv'
    print(f'Gerado arquivo de atvs fisicas simplificado => {nome_arquivo}...')
    df_atvs_ano.drop(lista_colunas_dropar_03, axis=1, inplace=True)
    df_atvs_ano.to_csv(nome_arquivo)


# ==================================
def salvar_arquivos_somatorios_anos():
  
    df_atividades_2020 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2020.csv', sep=',', encoding="ISO-8859-1")
    df_atividades_2021 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2021.csv', sep=',', encoding="ISO-8859-1")
    df_atividades_2022 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2022.csv', sep=',', encoding="ISO-8859-1")
    df_atividades_2023 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2023.csv', sep=',', encoding="ISO-8859-1")
    df_atividades_2024 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2024.csv', sep=',', encoding="ISO-8859-1")
    df_atividades_2025 = pd.read_csv('datasets/predados/atividades_fisicas_simplificado_2025.csv', sep=',', encoding="ISO-8859-1")

    lista_dfs_anos = [
        (2020,df_atividades_2020),
        (2021,df_atividades_2021),
        (2022,df_atividades_2022),
        (2023,df_atividades_2023),
        (2024,df_atividades_2024),
        (2025,df_atividades_2025)
    ]

    for item in lista_dfs_anos:
        ano = item[0]
        df_atividades_ano = item[1]
        lista_dfs = retorna_atividades_df_por_mes(df_atividades_ano)

        # Define os nomes das colunas
        colunas = ['ano','mes','Distance', 'tempo_min', 'Calories']
        # Cria um dicionário vazio com as colunas
        dados = {coluna: [] for coluna in colunas}

        # Cria o DataFrame vazio
        df_novo = pd.DataFrame(dados)
        df_concatenados = pd.DataFrame(dados)

        nome_arquivo = f'datasets/predados/atividades_fisicas_somatorio_{ano}.csv'
        indice = 0
        for mes in range(0, 12):

            df = lista_dfs[mes]

            soma_distancia = df['Distance'].sum()
            soma_tempo = df['tempo_min'].sum()
            soma_calorias = df['Calories'].sum()

            df_novo.loc[indice, ['ano', 'mes', 'Distance', 'tempo_min', 'Calories']] = [ano, mes, soma_distancia, soma_tempo, soma_calorias]
            indice += 1
            df_concatenados = pd.concat([df_novo], axis=0)

        df_concatenados.to_csv(nome_arquivo)

# ==================================
def compactar_pasta(pasta_origem, nome_base):
    """
    Compacta uma pasta em um arquivo ZIP com o nome contendo uma base e a data atual.

    Args:
        pasta_origem (str): O caminho da pasta a ser compactada.
        nome_base (str): A parte base do nome do arquivo ZIP.
    """
    data_atual = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo_zip = f"{nome_base}-{data_atual}.zip"
    caminho_arquivo_zip = os.path.join(os.getcwd(), nome_arquivo_zip)  # Salva na pasta atual

    with zipfile.ZipFile(caminho_arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as arquivo_zip:
        for pasta_raiz, subpastas, arquivos in os.walk(pasta_origem):
            for arquivo in arquivos:
                caminho_completo = os.path.join(pasta_raiz, arquivo)
                caminho_relativo = os.path.relpath(caminho_completo, pasta_origem)
                arquivo_zip.write(caminho_completo, caminho_relativo)

    print(f"Pasta '{pasta_origem}' compactada com sucesso em '{caminho_arquivo_zip}'")
# ==================================

def convert_tcx_to_gpx(file_to_convert):
    """
    Converte um arquivo TCX para GPX.
    """
    # Importa a biblioteca tcx2gpx
    from tcx2gpx.tcx2gpx import TCX2GPX

    # Cria um objeto TCX2GPX e converte o arquivo
    gps_object = TCX2GPX(tcx_path=file_to_convert)
    gps_object.convert()

    from tcx2gpx.tcx2gpx import TCX2GPX

    gps_object = TCX2GPX(tcx_path=file_to_convert)
    gps_object.convert()
# ==================================

# ==================================
# ATENÇÂO
# ==================================

# ==================================
# Antes de executar o código, executar o passo de compactar a pasta datasets
# 1. Compactar a pasta datasets
# 2. Salvar os arquivos de atividades completos por ano
# ==================================
compactar_pasta("datasets", "bkp_datasets")

# ==================================
def executa_preprocessamento_dados():
  salvar_arquivos_atividades_completos_anos()
  salvar_arquivos_atividades_simplificados_anos()
  salvar_arquivos_somatorios_anos()
# ==================================

# ==================================
if __name__ == "__main__":
  # Executa o código
  compactar_pasta("datasets", "bkp_datasets")
  executa_preprocessamento_dados()
# ==================================  
