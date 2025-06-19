# =======================================================
# Imports
# =======================================================
import altair as alt
import random
import streamlit as st

from vega_datasets import data
from config.painel_strava_agrupamentos import *

# =======================================================
# Constantes
# =======================================================

lista_cores_graficos = [
    '#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d', '#d95b43', '#5bc0de', '#4caf50', '#ffeb3b', '#c497d9',
    '#00BFFF', '#32CD32', '#FF00FF', '#FFA500', '#5A87E8', '#00CED1', '#FF7F50', '#228B22', '#FFD700', '#000080',
    '#FF1493', '#4B0082', '#8A2BE2', '#7FFF00', '#00FFFF', '#008000'
]

# =======================================================
# Gráficos de pizza
# =======================================================
def grafico_pizza_tipo_atv(df_atvs):

    grafico = alt.Chart(df_atvs).mark_arc().encode(
        theta="qtd",
        color=alt.Color('tipo_atividade:N', title='Tipo de Atividade')     
    )   

    return grafico
# ==================================================


# =======================================================
# Gráficos de barras
# =======================================================
def gera_grafico_barras_tipo_exercicio(df_filtro, titulo):

    grafico = alt.Chart(df_filtro).mark_bar().encode(
        x=alt.X('tipo_atividade:N', title='Tipo'),
        y=alt.Y('qtd:Q', title='Quantidade de Atividades'),
        tooltip=['tipo_atividade', 'qtd'],      
        color=alt.Color('tipo_atividade:N', title='Tipo de Atividade')     
    ).properties(
        title=alt.Title(
            text=titulo
        ),
        width=800,
        height=600
    ).interactive()

    return grafico    
# =======================================================
def gera_grafico_barras_atividades_mes(df_filtro, titulo):

    grafico = alt.Chart(df_filtro).mark_bar().encode(
        x=alt.X('mes:N', title='Mês'),
        y=alt.Y('qtd:Q', title='Quantidade de Atividades'),
        tooltip=['mes', 'qtd'],      
        color=alt.Color('mes:N', title='Mês')     
    ).properties(
        title=alt.Title(
            text=titulo
        ),
        width=700,
        height=500
    ).interactive()

    return grafico    
# =======================================================

# =======================================================
# Gráficos de Fluxo
# =======================================================
def gera_graficos_fluxo_por_tipo(titulo, df_atividades):

    grafico = alt.Chart(df_atividades).mark_area().encode(
        alt.X('ano:N').axis(domain=False, tickSize=0),
        alt.Y('sum(qtd):Q').stack('center').axis(None),
        alt.Color('tipo_atividade:N').scale(scheme='category20b').title('Tipo')
    ).properties(
        title=titulo,
        width=800, height=600            
    ).interactive()

    return grafico
# =======================================================
def gera_graficos_fluxo_por_dia_semana(titulo, df_atividades):

    grafico = alt.Chart(df_atividades).mark_area().encode(
        alt.X('ano:N').axis(domain=False, tickSize=0),
        alt.Y('sum(qtd):Q').stack('center').axis(None),
        alt.Color('dia_semana:N').scale(scheme='category20b').title('Dia da Semana')
    ).properties(
        title=titulo,
        width=800, height=600            
    ).interactive()

    return grafico
# =======================================================

# =======================================================
# Gráficos de Barra Empilhadas
# =======================================================
def grafico_barras_empilhadas_por_tupo(titulo, df):

    grafico = alt.Chart(df).mark_bar(width=20).encode(
        alt.X('ano:N', title='Ano'),
        alt.Y('sum(qtd)', title='Soma das Quantidades'),
        alt.Color('tipo_atividade', title='Tipo Atividade')
    ).properties(
            title=titulo,
            width=800, height=600
    ).interactive()   
    
    return grafico
# =======================================================
def grafico_barras_empilhadas_por_dia_semana(titulo, df):

    grafico = alt.Chart(df).mark_bar(width=20).encode(
        alt.X('ano:N', title='Ano'),
        alt.Y('sum(qtd)', title='Soma das Quantidades'),
        alt.Color('dia_semana', title='Dia da Semana')
    ).properties(
            title=titulo,
            width=800, height=600
    ).interactive()   
    
    return grafico
# =======================================================


# =======================================================
# Gráficos de Mapa de Calor (Heatmap)
# =======================================================
def gera_graficos_mapa_calor_por_tipo_atv(df_atividades, titulo):
                                            
    heatmap = alt.Chart(df_atividades).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('tipo_atividade:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Atividades' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_atividades).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='tipo_atividade:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=titulo
    )

    return heatmap_with_text                                    
# ==========================================================================
def gera_graficos_mapa_calor_por_dia_semana_atv(df_atividades, titulo):
                                            
    heatmap = alt.Chart(df_atividades).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('dia_semana:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Atividades' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_atividades).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='dia_semana:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=titulo
    )

    return heatmap_with_text                                    
# ==========================================================================


# =======================================================
def gera_grafico_por_dia_semana(titulo, contagem_por_dia_semana):

    lista_cores = alt.Scale(domain=contagem_por_dia_semana['dia_semana'].unique(),
    range=lista_cores_graficos)
                                
    chart = alt.Chart(contagem_por_dia_semana).mark_bar().encode(
        y=alt.Y('dia_semana:N', title='Dia da Semana',  sort='-x', axis=alt.Axis(labelLimit=200)),
        x=alt.X('qtd:Q', title='Quantidade de Acidentes',  axis=alt.Axis(labelAngle=-45)),
        tooltip=['dia_semana', 'qtd'],
        color=alt.Color('dia_semana:N', title='Dia da Semana', scale=lista_cores)

    ).properties(
        title=titulo,
        width=800,
        height=600         
    ).interactive()

    return chart
# =======================================================    
def grafico_barras_empilhadas_por_dia_semana(titulo, df):
        
    grafico = alt.Chart(df).mark_bar(width=20).encode(
        alt.X('ano:N', title='Ano'),
        alt.Y('sum(qtd)', title='Soma das Quantidades'),
        alt.Color('dia_semana', title='Dia da Semana')
    ).properties(
            title=titulo,
            width=800, height=600
    ).interactive()   

    return grafico
# ==========================================================================

    
# ==========================================================================

# ==========================================================================
# Gráficos de Ranking
# ==========================================================================

# ==========================================================================
def gera_grafico_ranking_tipo_01(df_atividades, titulo):

    grafico = alt.Chart(df_atividades).mark_line(point=True).encode(
        x=alt.X('ano:O', title='Ano'),
        y=alt.Y("rank:O", title='Posição do Ranking'),
        color=alt.Color("tipo_atividade:N", title='Tipo') 
    ).transform_window(
        rank="rank()",
        sort=[alt.SortField("qtd", order="descending")],
        groupby=["ano"]
    ).properties(
        title=titulo,
        width=800,
        height=600,
    )

    return grafico
# ==========================================================================
def gera_grafico_ranking_dia_semana_01(df_atividades, titulo):

    grafico_ranking_01 = alt.Chart(df_atividades).mark_line(point=True).encode(
        x=alt.X('ano:O', title='Ano'),
        y=alt.Y("rank:O", title='Posição do Ranking'),
        color=alt.Color("dia_semana:N", title="Dia da Semana")
    ).transform_window(
        rank="rank()",
        sort=[alt.SortField("qtd", order="descending")],
        groupby=["ano"]
    ).properties(
        title=titulo,
        width=800, height=600,
    )

    return grafico_ranking_01
# ==========================================================================
def gera_grafico_ranking_diasemana_02(df_acidentes_geral_por_dia_semana):

    grafico_ranking_dia_semana_02 = alt.Chart(df_acidentes_geral_por_dia_semana).mark_line(point=True).encode(
        x=alt.X('ano:N', axis=alt.Axis(title='Ano')),
        y=alt.Y('qtd:Q', axis=alt.Axis(title='Quantidade de Acidentes')),
        color=alt.Color("dia_semana:N", title="Dia da Semana"),
        tooltip=['dia_semana', 'qtd', 'ano']
    ).properties(
        title='Evolução da Quantidade de Acidentes por Dia da Semana (2007-2024)',
        width=800, height=600
    ).add_selection(
        alt.selection_single(fields=['ano'], bind='legend')
    ).interactive()

    return grafico_ranking_dia_semana_02
# ==========================================================================

# ==========================================================================
# Gráficos de Distribuição
# ==========================================================================

# ==========================================================================
def gera_graficos_distribuicao_por_uf(df_acidentes_geral_por_uf):

    grafico01 = alt.Chart(df_acidentes_geral_por_uf).mark_boxplot(extent='min-max').encode(
        alt.X('uf:N', title='Unidade Federativa (UF)'),
        alt.Y('qtd:Q', title='Quantidade de Acidentes'),        
    ).properties(
        width=800,
        height=600,
        title='Distribuição de Acidentes por UF (2007 a 2024)'
    )

    return grafico01
# ==========================================================================
def gera_graficos_distribuicao_por_tipo(df_acidentes_geral_por_tipo):

    grafico02 = alt.Chart(df_acidentes_geral_por_tipo).mark_boxplot(extent='min-max').encode(
        alt.X('tipo_acidente:N', title='Tipos de Acidentes'),
        alt.Y('qtd:Q', title='Quantidade de Acidentes')        
    ).properties(
        width=800,
        height=600,
        title='Distribuição de Acidentes por Tipo (2007 a 2024)'
    )

    return grafico02
# ==========================================================================
def gera_graficos_distribuicao_por_br(df_acidentes_geral_por_br):

    grafico03 = alt.Chart(df_acidentes_geral_por_br).mark_boxplot(extent='min-max').encode(
        alt.X('br:N', title='Rodovias Federais (BR)'),
        alt.Y('qtd:Q', title='Quantidade de Acidentes')        
    ).properties(
        width=800,
        height=600,
        title='Distribuição de Acidentes por BR (2007 a 2024)'
    )

    return grafico03
# ==========================================================================
def gera_graficos_distribuicao_por_classificacao(df_acidentes_geral_por_classificacao):
    
    grafico04 = alt.Chart(df_acidentes_geral_por_classificacao).mark_boxplot(extent='min-max').encode(
        alt.X('classificacao_acidente:N', title='Classificações de Acidentes'),        
        alt.Y('qtd:Q', title='Quantidade de Acidentes')        
    ).properties(
        width=800,
        height=600,
        title='Distribuição de Acidentes por Classificação (2007 a 2024)'
    )

    return grafico04
# ==========================================================================
def gera_graficos_distribuicao_por_causa(df_acidentes_geral_por_causa):

    grafico05 = alt.Chart(df_acidentes_geral_por_causa).mark_boxplot(extent='min-max').encode(
        alt.X('causa_acidente:N', title='Causas de Acidentes'),  
        alt.Y('qtd:Q', title='Quantidade de Acidentes')        
    ).properties(
        width=800,
        height=600,
        title='Distribuição de Acidentes por Causa (2007 a 2024)'
    )

    return grafico05
# ==========================================================================
def gera_graficos_distribuicao_por_fasedia(df_acidentes_geral_por_fasedia):

    grafico06 = alt.Chart(df_acidentes_geral_por_fasedia).mark_boxplot(extent='min-max').encode(
        alt.X('fase_dia:N', title='Fases do Dia'), 
        alt.Y('qtd:Q', title='Quantidade de Acidentes')        
    ).properties(
        width=800,
        height=600,
        title='Distribuição de Acidentes por Fase do Dia (2007 a 2024)'
    )

    return grafico06
# ==========================================================================
def gera_graficos_distribuicao_por_condicao_metereologica(df_acidentes_geral_por_condicaometereologica):

    grafico07 = alt.Chart(df_acidentes_geral_por_condicaometereologica).mark_boxplot(extent='min-max').encode(
        alt.X('condicao_metereologica:N', title='Condições Metereológicas'), 
        alt.Y('qtd:Q', title='Quantidade de Acidentes')        
    ).properties(
        width=800,
        height=600,
        title='Distribuição de Acidentes por Condição Metereológica (2007 a 2024)'
    )

    return grafico07
# ==========================================================================
def gera_graficos_distribuicao_por_dia_semana(df_acidentes_geral_por_dia_semana):    

    grafico08 = alt.Chart(df_acidentes_geral_por_dia_semana).mark_boxplot(extent='min-max').encode(
        alt.X('dia_semana:N', title='Dia da Semana'), 
        alt.Y('qtd:Q', title='Quantidade de Acidentes')        
    ).properties(
        width=800,
        height=600,
        title='Distribuição de Acidentes por Dia da Semana (2007 a 2024)'
    )

    return grafico08
# ==========================================================================
def gera_graficos_distribuicao_por_tipo_veiculo(df_acidentes_geral_por_tipo_veiculo):

    grafico09 = alt.Chart(df_acidentes_geral_por_tipo_veiculo).mark_boxplot(extent='min-max').encode(
        alt.X('tipo_veiculo:N', title='Tipo de Veículo'), 
        alt.Y('qtd:Q', title='Quantidade de Acidentes')        
    ).properties(
        width=800,
        height=600,
        title='Distribuição de Acidentes por Tipo de Veículo (2007 a 2024)'
    )

    return grafico09
# ==========================================================================
def gera_graficos_mapa_calor_por_uf(df_acidentes_geral_por_uf):

    heatmap = alt.Chart(df_acidentes_geral_por_uf).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('uf:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Acidentes' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_acidentes_geral_por_uf).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='uf:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=f'Mapa de Calor de Acidentes por UF (2007-2024)'
    )

    return heatmap_with_text    
# ==========================================================================    
def gera_graficos_mapa_calor_por_tipo(df_acidentes_geral_por_tipo):
    
    heatmap = alt.Chart(df_acidentes_geral_por_tipo).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('tipo_acidente:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Acidentes' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_acidentes_geral_por_tipo).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='tipo_acidente:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=f'Mapa de Calor de Acidentes por Tipo (2007-2024)'
    )

    return heatmap_with_text
# ==========================================================================    
def gera_graficos_mapa_calor_por_br(df_acidentes_geral_por_br):
        
    heatmap = alt.Chart(df_acidentes_geral_por_br).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('br:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Acidentes' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_acidentes_geral_por_br).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='br:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=f'Mapa de Calor de Acidentes por BR (2007-2024)'
    )

    return heatmap_with_text
# ==========================================================================
def gera_graficos_mapa_calor_por_classificacao(df_acidentes_geral_por_classificacao):
            
    heatmap = alt.Chart(df_acidentes_geral_por_classificacao).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('classificacao_acidente:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Acidentes' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_acidentes_geral_por_classificacao).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='classificacao_acidente:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=f'Mapa de Calor de Acidentes por Classificação (2007-2024)'
    )

    return heatmap_with_text
# ==========================================================================
def gera_graficos_mapa_calor_por_causa(df_acidentes_geral_por_causa):
            
    heatmap = alt.Chart(df_acidentes_geral_por_causa).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('causa_acidente:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Acidentes' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_acidentes_geral_por_causa).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='causa_acidente:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=f'Mapa de Calor de Acidentes por Causa (2007-2024)'
    )

    return heatmap_with_text
# ==========================================================================
def gera_graficos_mapa_calor_por_fasedia(df_acidentes_geral_por_fasedia):
                
    heatmap = alt.Chart(df_acidentes_geral_por_fasedia).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('fase_dia:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Acidentes' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_acidentes_geral_por_fasedia).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='fase_dia:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=f'Mapa de Calor de Acidentes por Fase do Dia (2007-2024)'
    )

    return heatmap_with_text
# ==========================================================================
def gera_graficos_mapa_calor_por_condicao_metereologica(df_acidentes_geral_por_condicao_metereologica):
                        
    heatmap = alt.Chart(df_acidentes_geral_por_condicao_metereologica).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('condicao_metereologica:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Acidentes' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_acidentes_geral_por_condicao_metereologica).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='condicao_metereologica:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=f'Mapa de Calor de Acidentes por Condição Metereológica (2007-2024)'
    )

    return heatmap_with_text
# ==========================================================================
def gera_graficos_mapa_calor_por_dia_semana(df_acidentes_geral_por_dia_semana):
                                
    heatmap = alt.Chart(df_acidentes_geral_por_dia_semana).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('dia_semana:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Acidentes' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_acidentes_geral_por_dia_semana).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='dia_semana:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=f'Mapa de Calor de Acidentes por Dia da Semana (2007-2024)'
    )

    return heatmap_with_text                
# ==========================================================================
def gera_graficos_mapa_calor_por_tipo_veiculo(df_acidentes_geral_por_tipo_veiculo):
                                            
    heatmap = alt.Chart(df_acidentes_geral_por_tipo_veiculo).mark_rect().encode(
        x=alt.X('ano:O', title=None, axis=alt.Axis(orient='top')),  # Define a orientação do eixo x como 'top'
        y=alt.Y('tipo_veiculo:N', title=None),
        color=alt.Color('qtd:Q', title='Qtd de Acidentes' ,scale=alt.Scale(scheme='yellowgreenblue')),    
    )

    # Adiciona o texto dentro de cada célula com o valor real e ajusta a cor do texto
    text = alt.Chart(df_acidentes_geral_por_tipo_veiculo).mark_text(baseline='middle', fontSize=10).encode(
        x='ano:O',
        y='tipo_veiculo:O',
        text=alt.Text('qtd:Q', format='.0f'),
    )

    # Combina o gráfico de calor com o texto
    heatmap_with_text = (heatmap + text).properties(
        width=800,
        height=600,
        title=f'Mapa de Calor de Acidentes por Tipo de Veículo (2007-2024)'
    )

    return heatmap_with_text                                    
# ==========================================================================

@st.cache_data
def plotar_brs(lista_brs):

    import geopandas as gpd
    import altair as alt
    from altair_saver import save
    import json

    # Carregando os dados do arquivo JSON
    with open('br_states.json') as f:
        geojson = json.load(f)
        
    # Convertendo para um GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(geojson['features'])

    # Criando o mapa
    chart1 = alt.Chart(gdf).mark_geoshape(
        filled=True,
        stroke='black'
    ).properties(
        width=1024,
        height=768,
        title='Mapa das BRs do Brasil'
    ).project(
        type='mercator'  # Altere para a projeção desejada
    )

    # Carregar o arquivo SHP
    df_info = gpd.read_file('coordenadas-rodovias/SNV_202404A.dbf')

    grafs = []

    for item in lista_brs:
        df_info_filtrado_br = df_info[(df_info['ds_jurisdi'] == 'Federal') & (df_info['vl_br'] == str(item))]

        df_info_filtrado_br_geometry = df_info_filtrado_br[['geometry','vl_br']]
        serie_br_geometry = df_info_filtrado_br['geometry'].simplify(tolerance=0.01)
        df_info_filtrado_br_geometry['geometry'] = serie_br_geometry
        df_info_filtrado_br_geometry['br'] = 'BR-'+str(item)
        grafico = gera_grafico_uma_br(df_info_filtrado_br_geometry)
        grafs.append(grafico)

    print(f'lista_graficos = {len(grafs)}')

    juntos = chart1
    if len(grafs) == 1:
        juntos = chart1 + grafs[0] 
    elif len(grafs) == 2:
        juntos = chart1 + grafs[0] + grafs[1] 
    elif len(grafs) == 3:
        juntos = chart1 + grafs[0] + grafs[1] + grafs[2] 
    elif len(grafs) == 4:
        juntos = chart1 + grafs[0] + grafs[1] + grafs[2] + grafs[3] 
    elif len(grafs) == 5:
        juntos = chart1 + grafs[0] + grafs[1] + grafs[2] + grafs[3] + grafs[4] 
    elif len(grafs) == 6:
        juntos = chart1 + grafs[0] + grafs[1] + grafs[2] + grafs[3] + grafs[4] + grafs[5] 
    elif len(grafs) == 7:
        juntos = chart1 + grafs[0] + grafs[1] + grafs[2] + grafs[3] + grafs[4] + grafs[5] + grafs[6] 
    elif len(grafs) == 8:
        juntos = chart1 + grafs[0] + grafs[1] + grafs[2] + grafs[3] + grafs[4] + grafs[5] + grafs[6] + grafs[7]  
    elif len(grafs) == 9:
        juntos = chart1 + grafs[0] + grafs[1] + grafs[2] + grafs[3] + grafs[4] + grafs[5] + grafs[6] + grafs[7] + grafs[8] 
    elif len(grafs) == 10:
        juntos = chart1 + grafs[0] + grafs[1] + grafs[2] + grafs[3] + grafs[4] + grafs[5] + grafs[6] + grafs[7] + grafs[8] + grafs[9]

    juntos.save('mapas/mapa_brasil_brs_10.png')

    return juntos

# ==================================================
def gera_grafico_uma_br(df_geometry_br):

    cores = [
        'black', 'silver', 'gray', 'white', 'maroon', 'red', 'purple', 'fuchsia', 'green', 'lime', 'olive', 'yellow', 
        'navy', 'blue', 'teal', 'aqua', 'orange', 'aliceblue', 'antiquewhite', 'aquamarine', 'azure', 'beige', 'bisque',
        'blanchedalmond', 'blueviolet', 'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 
        'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 
        'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 
        'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 
        'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'greenyellow', 'grey', 
        'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 
        'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 
        'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 
        'limegreen', 'linen', 'magenta', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 
        'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 
        'moccasin', 'navajowhite', 'oldlace', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 
        'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'rosybrown', 'royalblue', 'saddlebrown', 
        'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 
        'steelblue', 'tan', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'whitesmoke', 'yellowgreen', 'rebeccapurple']    
    

    indice = random.randint(0, len(cores)-1 )
    cor_selecionada = cores[indice]

    chart = alt.Chart(df_geometry_br).mark_geoshape(
        filled=True,
        strokeWidth=2.0,
        stroke=cor_selecionada,
    ).properties(
        width=1024,
        height=768,
    ).encode(
        color='br:N',
        tooltip=['br:N']
    ).project(
        type='mercator'  # Altere para a projeção desejada
    )

    return chart
# ==================================================

