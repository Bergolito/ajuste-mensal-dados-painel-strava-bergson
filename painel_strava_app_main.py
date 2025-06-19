# =======================================================
# Imports
# =======================================================
import pandas as pd
import streamlit as st
import folium
import streamlit as st

from streamlit_folium import folium_static
from config.painel_strava_funcoes import *
from painel_strava_graficos import *

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

df_sumario_2024 = pd.read_csv('datasets/gerais/sumario_atividades_2024.csv', sep=',', encoding="UTF-8")

df_atvs_tipo_todos = pd.read_csv('datasets/gerais/atividades_geral_por_tipo.csv', sep=',', encoding="UTF-8")
df_atvs_dia_semana_todos = pd.read_csv('datasets/gerais/atividades_geral_por_dia_semana.csv', sep=',', encoding="UTF-8")

df_sumario_atvs_2020 = pd.read_csv('datasets/gerais/sumario_atividades_2020.csv', sep=',', encoding="UTF-8")
df_sumario_atvs_2021 = pd.read_csv('datasets/gerais/sumario_atividades_2021.csv', sep=',', encoding="UTF-8")
df_sumario_atvs_2022 = pd.read_csv('datasets/gerais/sumario_atividades_2022.csv', sep=',', encoding="UTF-8")
df_sumario_atvs_2023 = pd.read_csv('datasets/gerais/sumario_atividades_2023.csv', sep=',', encoding="UTF-8")
df_sumario_atvs_2024 = pd.read_csv('datasets/gerais/sumario_atividades_2024.csv', sep=',', encoding="UTF-8")
df_sumario_atvs_2025 = pd.read_csv('datasets/gerais/sumario_atividades_2025.csv', sep=',', encoding="UTF-8")

# =======================================================
# Constantes do dashboard
# =======================================================

# CSS para estilizar a tabela
css = """
<style>
.estilo_tabela {
width: 100%;
border-collapse: collapse;
}
.estilo_tabela th, .estilo_tabela td {
border: 1px solid #ddd;
padding: 8px;
text-align: left;
}
.estilo_tabela th {
background-color: #f2f2f2;
font-weight: bold;
}
.estilo_tabela tr:nth-child(even) {
background-color: #f9f9f9;
}
</style>
"""

OPCAO_TODOS = 'Todos'
OPCAO_NONE = None
COLUNA_ANO = 'ano'

OPCAO_FILTRO_POR_UM_ANO = "Filtro por Um Ano"
OPCAO_FILTRO_POR_PERIODO = "Filtro por Período"
opcoes = [OPCAO_FILTRO_POR_UM_ANO, OPCAO_FILTRO_POR_PERIODO]

ano_inicio = None
ano_fim = None

st.set_page_config(
    page_title="Atividades Físicas Strava",
    #page_icon="🧊",
    page_icon="🏃",
    #page_icon="sports_medal"	

    layout="wide",  # or "centered"
    initial_sidebar_state="expanded",  # or "collapsed"
    menu_items={
        'Get Help': 'https://www.streamlit.io/help',
        'Report a bug': 'https://github.com/streamlit/streamlit/issues',
        'About': '# This is a header',
    }
)

# Definir o título fixo para o painel
st.title("Atividades Físicas Bergson (Strava)")

exibir_filtro_periodo_anos = False

with st.sidebar:
    st.header("Filtros:")
    
    opcao_selecionada = st.radio(
        "Selecione uma opção:",
        opcoes,
        index=0,
        disabled=False # Inicialmente habilitado
    )
    indice_selecionado = opcoes.index(opcao_selecionada)
    print(f'indice_selecionado => {indice_selecionado}')

    st.session_state.opcao_selecionada = opcao_selecionada

    if st.session_state.opcao_selecionada == OPCAO_FILTRO_POR_UM_ANO:

        ano_selecionado = st.sidebar.selectbox(
            'Qual o ano deseja visualizar?',
            (OPCAO_TODOS,'2025','2024', '2023', '2022', '2021', '2020'), index=1,
            key="ano_selecionado"
        )

        print(f'Ano Selecionado = {ano_selecionado}')

        exibir_filtro_periodo_anos = False

    else:
        exibir_filtro_periodo_anos = True
        st.sidebar.title("Filtro por Período de Anos:")
        ano_selecionado = None

        col1, col2 = st.sidebar.columns(2)  # Divide a linha em duas colunas para melhor layout

        with col1:
            ano_inicio = st.sidebar.number_input("Ano de Início", key=ano_inicio, min_value=2020, max_value=2025, step=1, value=2020)
        with col2:
            ano_fim = st.sidebar.number_input("Ano de Fim", key=ano_fim, min_value=2020, max_value=2025, step=1, value=2024)

        # Validação básica para garantir que o ano de início não seja posterior ao ano de fim
        if ano_inicio > ano_fim:
            st.sidebar.error("Erro: O ano de início não pode ser posterior ao ano de fim.")
            ano_inicio = None  # Reseta os valores para evitar processamento incorreto
            ano_fim = None


st.sidebar.write(f"Opção selecionada: {st.session_state.opcao_selecionada}")

if 'ano_selecionado' not in st.session_state:
    st.session_state.ano_selecionado = None

# Definição de abas
primeira_aba, segunda_aba, tab_03, tab_04, tab_05, tab_06, tab_detalhamento, aba_grid_mensal = st.tabs(
  [
    "Atvs - Geral",
    "Atvs - Tipo",
    "Atvs - Ranking",
    "Atvs - Barras Empilhadas",
    "Atvs - Fluxo",
    "Atvs - Mapa de Calor",
    "Atvs - Detalhamento",
    "Atvs - Grid Mensal"
  ]
)

# filtro
df_selecionado = df_atividades_simplificado_2024
ano_selecionado1 = 2025
if st.session_state.ano_selecionado is None:
    df_selecionado = df_atividades_simplificado_2024
else:

    if st.session_state.ano_selecionado == 'Todos':
        ano_selecionado1 = 'Todos'
        df_selecionado = df_atividades_simplificado_todos

    elif st.session_state.ano_selecionado == '2020':
        ano_selecionado1 = 2020
        df_selecionado = df_atividades_simplificado_2020

    elif st.session_state.ano_selecionado == '2021':
        ano_selecionado1 = 2021
        df_selecionado = df_atividades_simplificado_2021    

    elif st.session_state.ano_selecionado == '2022':
        ano_selecionado1 = 2022
        df_selecionado = df_atividades_simplificado_2022    

    elif st.session_state.ano_selecionado == '2023':
        ano_selecionado1 = 2023
        df_selecionado = df_atividades_simplificado_2023    

    elif st.session_state.ano_selecionado == '2024':
        ano_selecionado1 = 2024
        df_selecionado = df_atividades_simplificado_2024    

    elif st.session_state.ano_selecionado == '2025':
        ano_selecionado1 = 2025
        df_selecionado = df_atividades_simplificado_2025    

# ==============================================================================
with primeira_aba:

    titulo = f'Lista de Atividades (Geral)'
    st.markdown(titulo, unsafe_allow_html=True)  

    lista_dfs_ano = [
        (df_sumario_atvs_2020, 2020),
        (df_sumario_atvs_2021, 2021),
        (df_sumario_atvs_2022, 2022),
        (df_sumario_atvs_2023, 2023),
        (df_sumario_atvs_2024, 2024),
        (df_sumario_atvs_2025, 2025),
    ]
    # ordena os registros pelo ano
    lista_dfs_ano.sort(key=lambda x: x[1], reverse=True)

    lista_registros = []
    if ano_selecionado == 'Todos':
        lista_registros = lista_dfs_ano
    elif ano_selecionado == '2020':
        lista_registros.append((df_sumario_atvs_2020, 2020))
    elif ano_selecionado == '2021':
        lista_registros.append((df_sumario_atvs_2021, 2021))
    elif ano_selecionado == '2022':
        lista_registros.append((df_sumario_atvs_2022, 2022))
    elif ano_selecionado == '2023':
        lista_registros.append((df_sumario_atvs_2023, 2023))
    elif ano_selecionado == '2024':
        lista_registros.append((df_sumario_atvs_2024, 2024))
    elif ano_selecionado == '2025':
        lista_registros.append((df_sumario_atvs_2025, 2025))        

    for item in lista_registros:
        df = item[0].copy()
        df_ano = df.drop(columns=["Unnamed: 0","ano"])
        df_ano['qtd'] = df_ano['qtd'].astype(int)
        df_ano['mes'] = df_ano['mes'].apply(obter_mes_por_numero)
        df_ano['calorias'] = df_ano['calorias'].round(2)

        df_ano_grafico = df_ano.copy()
        titulo = f'Atividades Físicas em {item[1]}'
        grafico_atividades_ano_mes = gera_grafico_barras_atividades_mes(df_ano_grafico, titulo)

        qtd = df_ano['qtd'].sum()
        distancia = df_ano['distancia'].sum()
        calorias = df_ano['calorias'].sum()
        print(f'qtd => {qtd} | distancia =>  {distancia} | calorias => {calorias}')

        df_ano_estatistica = pd.DataFrame(columns=['criterio','qtd','distancia','calorias'])
        df_ano_estatistica.loc[0, 'criterio'] = 'Mínimo'
        df_ano_estatistica.loc[0, 'qtd'] = df_ano['qtd'].min()
        df_ano_estatistica.loc[0, 'distancia'] = df_ano['distancia'].min()
        df_ano_estatistica.loc[0, 'calorias'] = df_ano['calorias'].min()

        df_ano_estatistica.loc[1, 'criterio'] = 'Máximo'
        df_ano_estatistica.loc[1, 'qtd'] = df_ano['qtd'].max()
        df_ano_estatistica.loc[1, 'distancia'] = df_ano['distancia'].max()
        df_ano_estatistica.loc[1, 'calorias'] = df_ano['calorias'].max()        

        df_ano_estatistica.loc[2, 'criterio'] = 'Média'
        df_ano_estatistica.loc[2, 'qtd'] = df_ano['qtd'].mean()
        df_ano_estatistica.loc[2, 'distancia'] = df_ano['distancia'].mean()
        df_ano_estatistica.loc[2, 'calorias'] = df_ano['calorias'].mean()                

        index = df_ano.shape[0]+1
        df_ano.loc[index,'mes'] = 'TOTAL'
        df_ano.loc[index,'qtd'] = qtd
        df_ano.loc[index,'distancia'] = distancia
        df_ano.loc[index,'calorias'] = calorias

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<h2> {item[1]} </h2>', unsafe_allow_html=True)  
            html_table_ano = df_ano.to_html(classes='estilo_tabela', index=False) 
            st.markdown(css, unsafe_allow_html=True)
            st.write(html_table_ano, unsafe_allow_html=True)

        with col2:
            st.altair_chart(grafico_atividades_ano_mes, use_container_width=False)

# ==============================================================================
with segunda_aba:

    # =======================================================
    # aba 01
    # =======================================================
    titulo = f'<h3> Atividades por Tipo'
    st.markdown(titulo, unsafe_allow_html=True)  

    titulo = f'Atividades Físicas em {ano_selecionado1}'
    st.write(f' Ano selecionado => {ano_selecionado1}') 
    if ano_selecionado1 != 'Todos':
        df_filtro = df_atvs_tipo_todos[(df_atvs_tipo_todos['ano'] == ano_selecionado1)]
    elif ano_selecionado1 == 'Todos':
        df_filtro = df_atvs_tipo_todos

    df_filtro2 = df_filtro.copy()
    index_linha1 = df_filtro2.shape[0]+1
    df_filtro2.loc[index_linha1,'tipo_atividade']='TOTAL'
    total = df_filtro2['qtd'].sum()
    df_filtro2.loc[index_linha1,'qtd']=total
    df_filtro2.loc[index_linha1,'ano']=''

    # Layout em duas colunas para melhor organização
    col1, col2 = st.columns(2)
    
    with col1:
        html_table1 = df_filtro2.to_html(classes='estilo_tabela', index=False) # index=False remove a coluna de índice
        st.write(html_table1, unsafe_allow_html=True)
        
        # Gráfico de pizza para distribuição por tipo
        st.subheader("Distribuição de Atividades por Tipo")
        grafico_pizza = grafico_pizza_tipo_atv(df_filtro)
        st.altair_chart(grafico_pizza, use_container_width=True)

    with col2:
        index_linha2 = df_sumario_2024.shape[0]+1
        df_sumario_2024.loc[index_linha2,'mes']='TOTAL'
        total_qtd = df_sumario_2024['qtd'].sum()
        total_distancia = df_sumario_2024['distancia'].sum()
        total_caloria = df_sumario_2024['calorias'].sum()
        df_sumario_2024.loc[index_linha2,'qtd']=total
        df_sumario_2024.loc[index_linha2,'distancia']=total_distancia
        df_sumario_2024.loc[index_linha2,'calorias']=total_caloria

        html_table2 = df_sumario_2024.to_html(classes='estilo_tabela', index=False) # index=False remove a coluna de índice
        st.write(html_table2, unsafe_allow_html=True)
        
        # Gráfico de barras para tipos de exercício
        st.subheader("Quantidade por Tipo de Exercício")
        grafico_ano = gera_grafico_barras_tipo_exercicio(df_filtro, titulo)
        st.altair_chart(grafico_ano, use_container_width=True)

    # Seção de métricas importantes - números destacados
    st.subheader("Métricas de Desempenho")
    
    # Criando uma linha com métricas principais
    metrica1, metrica2, metrica3, metrica4 = st.columns(4)
    
    # Calculando métricas relevantes
    if df_filtro is not None and not df_filtro.empty:
        # Extrair e formatar métricas
        total_atividades = total
        media_por_mes = round(total / 12, 1) if ano_selecionado1 != 'Todos' else round(total / (len(df_filtro['ano'].unique()) * 12), 1)
        
        # Apresentando métricas em cards
        with metrica1:
            st.metric(label="Total de Atividades", value=f"{total_atividades}")
        
        with metrica2:
            st.metric(label="Média Mensal", value=f"{media_por_mes}")
        
        with metrica3:
            if 'distancia' in df_sumario_2024.columns:
                total_distancia = round(total_distancia, 2)
                st.metric(label="Distância Total (km)", value=f"{total_distancia}")
        
        with metrica4:
            if 'calorias' in df_sumario_2024.columns:
                total_calorias = round(total_caloria, 0)
                st.metric(label="Calorias Totais", value=f"{total_calorias}")
    
    # Seção de análise de tendências
    st.subheader("Análise de Tendências")
    
    # Criando abas para diferentes visualizações de tendências
    tab_tendencia1, tab_tendencia2 = st.tabs(["Tendência por Período", "Comparação de Tipos"])
    
    with tab_tendencia1:
        # Aqui podemos ver a evolução das atividades por período (dias da semana, meses)
        if ano_selecionado1 != 'Todos':
            st.write("Distribuição de Atividades por Dia da Semana")
            df_dia_semana = df_atvs_dia_semana_todos[df_atvs_dia_semana_todos['ano'] == ano_selecionado1]
            grafico_dias_semana = gera_grafico_por_dia_semana(f"Atividades por Dia da Semana em {ano_selecionado1}", df_dia_semana)
            st.altair_chart(grafico_dias_semana, use_container_width=True)
        else:
            st.write("Evolução de Atividades ao Longo dos Anos")
            grafico_ranking_01 = gera_grafico_ranking_tipo_01(df_atvs_tipo_todos, "Evolução dos Tipos de Atividades ao Longo dos Anos")    
            st.altair_chart(grafico_ranking_01, use_container_width=True)
    
    with tab_tendencia2:
        # Comparação entre diferentes tipos de atividades
        if ano_selecionado1 != 'Todos':
            st.write(f"Mapa de Calor por Tipo de Atividade em {ano_selecionado1}")
            df_heatmap = df_atvs_tipo_todos[df_atvs_tipo_todos['ano'] == ano_selecionado1]
            grafico_heatmap = gera_graficos_mapa_calor_por_tipo_atv(df_heatmap, f"Intensidade de Atividades por Tipo em {ano_selecionado1}")
            st.altair_chart(grafico_heatmap, use_container_width=True)
        else:
            st.write("Comparação dos Tipos de Atividades ao Longo dos Anos")
            grafico_fluxo = gera_graficos_fluxo_por_tipo("Fluxo de Atividades por Tipo ao Longo dos Anos", df_atvs_tipo_todos)
            st.altair_chart(grafico_fluxo, use_container_width=True)
            
    # Análise de progresso
    st.subheader("Análise de Progresso")
    
    # Seção para mostrar o progresso comparando períodos
    if ano_selecionado1 != 'Todos' and int(ano_selecionado1) > 2020:
        ano_anterior = int(ano_selecionado1) - 1
        
        df_ano_atual = df_atvs_tipo_todos[df_atvs_tipo_todos['ano'] == ano_selecionado1]
        df_ano_anterior = df_atvs_tipo_todos[df_atvs_tipo_todos['ano'] == ano_anterior]
        
        if not df_ano_anterior.empty and not df_ano_atual.empty:
            total_atual = df_ano_atual['qtd'].sum()
            total_anterior = df_ano_anterior['qtd'].sum()
            
            variacao = ((total_atual - total_anterior) / total_anterior) * 100 if total_anterior > 0 else 100
            
            st.write(f"### Comparação com {ano_anterior}")
            col_prog1, col_prog2 = st.columns(2)
            
            with col_prog1:
                st.metric(
                    label=f"Variação de Atividades em relação a {ano_anterior}", 
                    value=f"{total_atual}",
                    delta=f"{variacao:.1f}%"
                )
            
            with col_prog2:
                # Agrupamento para comparativo
                df_comparativo = pd.DataFrame({
                    'Ano': [str(ano_anterior), str(ano_selecionado1)],
                    'Total': [total_anterior, total_atual]
                })
                
                # Gráfico de barras comparativo
                grafico_comparativo = alt.Chart(df_comparativo).mark_bar().encode(
                    x=alt.X('Ano:N', title='Ano'),
                    y=alt.Y('Total:Q', title='Total de Atividades'),
                    color=alt.Color('Ano:N', legend=None),
                    tooltip=['Ano', 'Total']
                ).properties(
                    title="Comparativo de Atividades entre Anos",
                    width=300,
                    height=300
                ).interactive()
                
                st.altair_chart(grafico_comparativo, use_container_width=True)
    else:
        st.info("Selecione um ano específico posterior a 2020 para ver análise comparativa de progresso.")

# ==============================================================================
with tab_03:

    # =======================================================
    # aba 03
    # =======================================================
    titulo = f'<h3> Atividades por Ranking'
    st.markdown(titulo, unsafe_allow_html=True)  

    titulo =f'Ranking de Atividades por tipo (2020 a 2025)'
    grafico_ranking_01 = gera_grafico_ranking_tipo_01(df_atvs_tipo_todos, titulo)    
    st.altair_chart(grafico_ranking_01, use_container_width=False)

    titulo =f'Ranking de Atividades por dia da semana (2020 a 2025)'
    grafico_ranking_02 = gera_grafico_ranking_dia_semana_01(df_atvs_dia_semana_todos, titulo)
    st.altair_chart(grafico_ranking_02, use_container_width=False)

# ==============================================================================
with tab_04:

    # =======================================================
    # aba 04
    # =======================================================
    titulo = f'<h3> Atividades por Barras Empilhadas'
    st.markdown(titulo, unsafe_allow_html=True)  

    titulo =f'Barras Empilhadas de Atividades por tipo (2020 a 2025)'
    grafico_barras_emp_01 = grafico_barras_empilhadas_por_tupo(titulo, df_atvs_tipo_todos)    
    st.altair_chart(grafico_barras_emp_01, use_container_width=False)

    titulo =f'Barras Empilhadas de Atividades por dia da semana (2020 a 2025)'
    grafico_barras_emp_02 = grafico_barras_empilhadas_por_dia_semana(titulo, df_atvs_dia_semana_todos)    
    st.altair_chart(grafico_barras_emp_02, use_container_width=False)

# ==============================================================================
with tab_05:

    # =======================================================
    # aba 05
    # =======================================================
    titulo = f'<h3> Atividades por Fluxo de Dados'
    st.markdown(titulo, unsafe_allow_html=True)  

    titulo =f'Fluxo de Atividades por tipo (2020 a 2025)'
    grafico_fluxo_01 = gera_graficos_fluxo_por_tipo(titulo, df_atvs_tipo_todos)    
    st.altair_chart(grafico_fluxo_01, use_container_width=False)

    titulo =f'Fluxo de Atividades por dia da semana (2020 a 2025)'
    grafico_fluxo_02 = gera_graficos_fluxo_por_dia_semana(titulo, df_atvs_dia_semana_todos)    
    st.altair_chart(grafico_fluxo_02, use_container_width=False)

# ==============================================================================
with tab_06:

    # =======================================================
    # aba 06
    # =======================================================
    titulo = f'<h3> Atividades por Mapa de Calor'
    st.markdown(titulo, unsafe_allow_html=True)  

    titulo =f'Mapa de Calor por Tipo de Atividades (2020 a 2025)'
    grafico_mapa_calor_01 = gera_graficos_mapa_calor_por_tipo_atv(df_atvs_tipo_todos, titulo)
    st.altair_chart(grafico_mapa_calor_01, use_container_width=False)

    titulo =f'Mapa de Calor por Dia da Semana (2020 a 2025)'
    grafico_mapa_calor_02 = gera_graficos_mapa_calor_por_dia_semana_atv(df_atvs_dia_semana_todos, titulo)
    st.altair_chart(grafico_mapa_calor_02, use_container_width=False)

# ==============================================================================
with tab_detalhamento:

    # =======================================================
    # aba Detalhamento das Atividades
    # =======================================================
    titulo = f'<h3>Detalhamento das Atividades</h3>'
    st.markdown(titulo, unsafe_allow_html=True)

    # CSS adicional para botão e layout do detalhamento
    st.markdown("""
    <style>
    .btn-detalhar {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 5px 10px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 14px;
        margin: 2px 2px;
        cursor: pointer;
        border-radius: 4px;
    }
    .detalhe-atividade {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Definindo os anos disponíveis para seleção
    anos_disponiveis = ['2020', '2021', '2022', '2023', '2024', '2025']
    
    # Organizando os filtros em 3 colunas
    col1, col2, col3 = st.columns(3)
    
    # Coluna 1: Filtro de ano
    with col1:
        filtro_ano = st.selectbox('Selecione o ano:', anos_disponiveis, index=5)  # Default para 2025
    
    # Coluna 2: Checkbox para habilitar filtro por mês
    with col2:
        filtrar_por_mes = st.checkbox('Filtrar por mês')
    
    # Coluna 3: Filtro de mês (aparece somente se o checkbox estiver marcado)
    with col3:
        if filtrar_por_mes:
            meses = {
                '01 - Janeiro': 1, 
                '02 - Fevereiro': 2, 
                '03 - Março': 3, 
                '04 - Abril': 4,
                '05 - Maio': 5, 
                '06 - Junho': 6, 
                '07 - Julho': 7, 
                '08 - Agosto': 8,
                '09 - Setembro': 9, 
                '10 - Outubro': 10, 
                '11 - Novembro': 11, 
                '12 - Dezembro': 12
            }
            filtro_mes = st.selectbox('Selecione o mês:', list(meses.keys()))
            mes_selecionado = meses[filtro_mes]
        else:
            mes_selecionado = None
            st.empty()  # Espaço vazio para manter alinhamento
    
    # Definir o DataFrame baseado no ano selecionado
    df_completo = None
    if filtro_ano == '2020':
        df_completo = df_atividades_completo_2020.copy()
    elif filtro_ano == '2021':
        df_completo = df_atividades_completo_2021.copy()
    elif filtro_ano == '2022':
        df_completo = df_atividades_completo_2022.copy()
    elif filtro_ano == '2023':
        df_completo = df_atividades_completo_2023.copy()
    elif filtro_ano == '2024':
        df_completo = df_atividades_completo_2024.copy()
    elif filtro_ano == '2025':
        df_completo = df_atividades_completo_2025.copy()
    
    # Filtrar por mês se necessário
    if filtrar_por_mes and mes_selecionado is not None and df_completo is not None:
        # Verificar se 'Activity Date' está no formato correto
        if 'Activity Date' in df_completo.columns:
            try:
                # Converter para datetime
                df_completo['Activity Date'] = pd.to_datetime(df_completo['Activity Date'], format='%b %d, %Y, %I:%M:%S %p', errors='coerce')
                # Extrair mês e filtrar
                df_completo = df_completo[df_completo['Activity Date'].dt.month == mes_selecionado]
            except Exception as e:
                st.error(f"Erro ao filtrar por mês: {str(e)}")
        else:
            # Tentar usar a coluna data_mes se disponível
            if 'data_mes' in df_completo.columns:
                df_completo = df_completo[df_completo['data_mes'] == mes_selecionado]
    
    # Verificar se temos dados para exibir
    if df_completo is not None and not df_completo.empty:
        # Preparar dados para a tabela
        df_tabela = df_completo.copy()
        
        # Verificar e converter 'Activity Date' para datetime
        if 'Activity Date' in df_tabela.columns:
            df_tabela['Activity Date'] = pd.to_datetime(df_tabela['Activity Date'], format='%b %d, %Y, %I:%M:%S %p', errors='coerce')
            # Criar coluna formatada para exibição
            df_tabela['Data Formatada'] = df_tabela['Activity Date'].dt.strftime('%d/%m/%Y')
            
            # Adicionar dia da semana
            df_tabela['Dia da Semana'] = df_tabela['Activity Date'].apply(
                lambda x: retorna_dia_da_semana(x.strftime('%b %d, %Y, %I:%M:%S %p')) if not pd.isna(x) else "")
        else:
            st.warning("Coluna 'Activity Date' não encontrada no conjunto de dados.")
            # Criar colunas vazias para manter a estrutura
            df_tabela['Data Formatada'] = ""
            df_tabela['Dia da Semana'] = ""
        
        # Selecionar colunas essenciais para exibição
        colunas_essenciais = ['Data Formatada', 'Dia da Semana', 'Activity Name', 'Activity Type','Filename']
        
        # Verificar se todas as colunas essenciais existem
        colunas_existentes = [col for col in colunas_essenciais if col in df_tabela.columns]
        
        # Criar dataframe para exibição
        if len(colunas_existentes) > 0:
            df_exibicao = df_tabela[colunas_existentes].copy()
            
            # Renomear colunas para português
            renomear_colunas = {
                'Data Formatada': 'Data',
                'Dia da Semana': 'Dia da Semana',
                'Activity Name': 'Nome da Atividade',
                'Activity Type': 'Tipo da Atividade',
                'Filename': 'Arquivo GPX',
                'Distance': 'Distância (km)',
                'Elapsed Time': 'Tempo (min)',
                'Average Speed': 'Velocidade Média (km/h)',
                'Max Speed': 'Velocidade Máxima (km/h)',
                'Calories': 'Calorias',
                'Elevation Gain': 'Ganho de Elevação (m)',
                'Max Heart Rate': 'FC Máxima (bpm)',
                'Average Heart Rate': 'FC Média (bpm)'
            }
            
            # Aplicar renomeação apenas para colunas que existem
            renomear = {k: v for k, v in renomear_colunas.items() if k in df_exibicao.columns}
            df_exibicao = df_exibicao.rename(columns=renomear)
            
            # Exibir a tabela usando o método dataframe do Streamlit
            st.dataframe(df_exibicao, use_container_width=True)
            
            # Área para exibir detalhes de uma atividade específica
            st.markdown('### Detalhes da Atividade')
            
            # Permitir ao usuário selecionar uma atividade para ver detalhes
            id_atividades = df_tabela['Activity ID'].astype(str).tolist()
            id_atividades_dict = {f"{row['Data Formatada']} - {row['Activity Type']} - {row['Activity ID']}": row['Activity ID'] 
                              for _, row in df_tabela.iterrows() if 'Activity Name' in row and 'Activity ID' in row}
            
            if id_atividades_dict:
                atividade_selecionada = st.selectbox('Selecione uma atividade para ver detalhes:', 
                                                 list(id_atividades_dict.keys()))
                
                id_selecionado = id_atividades_dict[atividade_selecionada]
                
                # Filtrar dados da atividade selecionada
                atividade_detalhes = df_tabela[df_tabela['Activity ID'] == id_selecionado].iloc[0]
                
                # Criar layout em duas colunas para os detalhes
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Informações Básicas")
                    st.write(f"**ID:** {atividade_detalhes.get('Activity ID', 'N/A')}")
                    st.write(f"**Nome:** {atividade_detalhes.get('Activity Name', 'N/A')}")
                    st.write(f"**Tipo:** {atividade_detalhes.get('Activity Type', 'N/A')}")
                    st.write(f"**Data:** {atividade_detalhes.get('Data Formatada', 'N/A')}")
                    st.write(f"**Dia da Semana:** {atividade_detalhes.get('Dia da Semana', 'N/A')}")
                    st.write(f"**GPX File:** {atividade_detalhes.get('Filename', 'N/A')}")

                    if 'Activity Description' in atividade_detalhes and not pd.isna(atividade_detalhes['Activity Description']):
                        st.write(f"**Descrição:** {atividade_detalhes['Activity Description']}")
                
                with col2:
                    st.subheader("Métricas da Atividade")
                    
                    # Verificar e exibir métricas disponíveis
                    if 'Distance' in atividade_detalhes and not pd.isna(atividade_detalhes['Distance']):
                        st.metric("Distância", f"{float(atividade_detalhes['Distance']):.2f} km")
                    
                    if 'Elapsed Time' in atividade_detalhes and not pd.isna(atividade_detalhes['Elapsed Time']):
                        tempo_seg = float(atividade_detalhes['Elapsed Time'])
                        tempo_min = tempo_seg / 60  # Convertendo segundos para minutos
                        st.metric("Tempo", f"{tempo_min:.2f} min")
                    
                    if 'Average Speed' in atividade_detalhes and not pd.isna(atividade_detalhes['Average Speed']):
                        st.metric("Velocidade Média", f"{float(atividade_detalhes['Average Speed']):.2f} km/h")
                    
                    if 'Max Speed' in atividade_detalhes and not pd.isna(atividade_detalhes['Max Speed']):
                        st.metric("Velocidade Máxima", f"{float(atividade_detalhes['Max Speed']):.2f} km/h")
                    
                    if 'Calories' in atividade_detalhes and not pd.isna(atividade_detalhes['Calories']):
                        st.metric("Calorias", f"{float(atividade_detalhes['Calories']):.0f}")
                
                # Verificar se existe arquivo GPX para a atividade
                filename = atividade_detalhes.get('Filename', '')
                tcx_id = None
                
                if isinstance(filename, str) and filename.startswith('activities/'):
                    # Extrair ID do arquivo
                    tcx_id = filename.replace('activities/', '').split('.')[0]
                    print(f"tcx_id => {tcx_id}")
                
                # Verificar se existe arquivo TCX na pasta 'arquivos-ok'
                if tcx_id:
                    import os
                    tcx_filepath_ok = f"activities-tcx/arquivos-ok/{tcx_id}.tcx"
                    csv_filepath = f"activities-tcx/arquivos-csv/{tcx_id}.csv"
                    
                    if os.path.exists(tcx_filepath_ok):
                        st.success(f"Arquivo TCX encontrado: {tcx_id}.tcx")
                        
                        # Verificar se existe o CSV correspondente
                        if os.path.exists(csv_filepath):
                            try:
                                # Carregar o dataframe do CSV
                                df_rota = pd.read_csv(csv_filepath)
                                st.success(f"Dados da rota carregados com sucesso! ({df_rota.shape[0]} pontos)")
                                
                                # Verificar se o DataFrame tem colunas de latitude e longitude
                                if 'latitude' in df_rota.columns and 'longitude' in df_rota.columns:
                                    # Criar um mapa com os pontos da rota
                                    st.subheader("Mapa da Rota")
                                    
                                    # Calcular o centro do mapa
                                    lat_medio = df_rota['latitude'].mean()
                                    lon_medio = df_rota['longitude'].mean()
                                    
                                    # Criar o mapa
                                    m = folium.Map(location=[lat_medio, lon_medio], zoom_start=14)
                                    
                                    # Adicionar os pontos como uma linha
                                    points = list(zip(df_rota['latitude'], df_rota['longitude']))
                                    
                                    # Adicionar uma linha conectando os pontos (traçar a rota)
                                    folium.PolyLine(
                                        points,
                                        weight=5,
                                        color='blue',
                                        opacity=0.7
                                    ).add_to(m)
                                    
                                    # Adicionar marcadores para o início e o fim da rota
                                    folium.Marker(
                                        location=[df_rota['latitude'].iloc[0], df_rota['longitude'].iloc[0]],
                                        popup='Início',
                                        icon=folium.Icon(color='green')
                                    ).add_to(m)
                                    
                                    folium.Marker(
                                        location=[df_rota['latitude'].iloc[-1], df_rota['longitude'].iloc[-1]],
                                        popup='Fim',
                                        icon=folium.Icon(color='red')
                                    ).add_to(m)
                                    
                                    # Exibir o mapa
                                    folium_static(m, width=900)
                                    
                                else:
                                    st.warning("O arquivo CSV não contém coordenadas de latitude e longitude.")
                            
                            except Exception as e:
                                st.error(f"Erro ao carregar o arquivo CSV: {str(e)}")
                        else:
                            st.warning(f"Arquivo CSV correspondente não encontrado: {csv_filepath}")
                    else:
                        st.info(f"Arquivo TCX não encontrado na pasta 'arquivos-ok': {tcx_filepath_ok}")
        else:
            st.error("Não foi possível exibir os dados. Nenhuma coluna essencial encontrada.")
    else:
        st.warning("Não há dados disponíveis para os filtros selecionados.")
# ==============================================================================
with aba_grid_mensal:

    # =======================================================
    # Grid Mensal - exibindo 12 gráficos em grid 3x4
    # =======================================================
    titulo = f'<h3>Atividades Físicas - Grid Mensal</h3>'
    st.markdown(titulo, unsafe_allow_html=True)  

    if ano_selecionado1 != 'Todos':
        st.write(f"### Atividades de {ano_selecionado1} organizadas por mês")
        
        # Função para criar um gráfico mensal com tamanho reduzido
        def gera_grafico_compacto_mes(mes, df, ano):
            nome_mes = obter_mes_por_numero(mes)
            titulo = f'{nome_mes} de {ano}'
            df_filtro = agrupamento_atividade_por_tipo_por_ano_mes(df, ano, mes)

            # Criar gráfico mais compacto para caber no grid
            grafico_mes = alt.Chart(df_filtro).mark_bar().encode(
                x=alt.X('tipo_atividade:N', title='Tipo', axis=alt.Axis(labelAngle=-45, labelFontSize=10)),
                y=alt.Y('qtd:Q', title='Qtd'),
                tooltip=['tipo_atividade', 'qtd'],      
                color=alt.Color('tipo_atividade:N', title='Tipo de Atividade')     
            ).properties(
                title=alt.Title(
                    text=titulo,
                    fontSize=14
                ),
                width=300,
                height=200
            ).interactive()
            
            return grafico_mes, df_filtro
        
        # Criar layout de grid 3x4 (3 colunas, 4 linhas)
        # Linha 1 (Jan, Fev, Mar)
        row1_col1, row1_col2, row1_col3 = st.columns(3)
        
        # Linha 2 (Abr, Mai, Jun)
        row2_col1, row2_col2, row2_col3 = st.columns(3)
        
        # Linha 3 (Jul, Ago, Set)
        row3_col1, row3_col2, row3_col3 = st.columns(3)
        
        # Linha 4 (Out, Nov, Dez)
        row4_col1, row4_col2, row4_col3 = st.columns(3)
        
        # Linha 1: Janeiro, Fevereiro, Março
        with row1_col1:
            grafico_jan, df_jan = gera_grafico_compacto_mes(1, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_jan, use_container_width=True)
            with st.expander("Dados Janeiro"):
                st.dataframe(df_jan, use_container_width=True)
        
        with row1_col2:
            grafico_fev, df_fev = gera_grafico_compacto_mes(2, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_fev, use_container_width=True)
            with st.expander("Dados Fevereiro"):
                st.dataframe(df_fev, use_container_width=True)
        
        with row1_col3:
            grafico_mar, df_mar = gera_grafico_compacto_mes(3, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_mar, use_container_width=True)
            with st.expander("Dados Março"):
                st.dataframe(df_mar, use_container_width=True)
        
        # Linha 2: Abril, Maio, Junho
        with row2_col1:
            grafico_abr, df_abr = gera_grafico_compacto_mes(4, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_abr, use_container_width=True)
            with st.expander("Dados Abril"):
                st.dataframe(df_abr, use_container_width=True)
        
        with row2_col2:
            grafico_mai, df_mai = gera_grafico_compacto_mes(5, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_mai, use_container_width=True)
            with st.expander("Dados Maio"):
                st.dataframe(df_mai, use_container_width=True)
        
        with row2_col3:
            grafico_jun, df_jun = gera_grafico_compacto_mes(6, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_jun, use_container_width=True)
            with st.expander("Dados Junho"):
                st.dataframe(df_jun, use_container_width=True)
        
        # Linha 3: Julho, Agosto, Setembro
        with row3_col1:
            grafico_jul, df_jul = gera_grafico_compacto_mes(7, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_jul, use_container_width=True)
            with st.expander("Dados Julho"):
                st.dataframe(df_jul, use_container_width=True)
        
        with row3_col2:
            grafico_ago, df_ago = gera_grafico_compacto_mes(8, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_ago, use_container_width=True)
            with st.expander("Dados Agosto"):
                st.dataframe(df_ago, use_container_width=True)
        
        with row3_col3:
            grafico_set, df_set = gera_grafico_compacto_mes(9, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_set, use_container_width=True)
            with st.expander("Dados Setembro"):
                st.dataframe(df_set, use_container_width=True)
        
        # Linha 4: Outubro, Novembro, Dezembro
        with row4_col1:
            grafico_out, df_out = gera_grafico_compacto_mes(10, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_out, use_container_width=True)
            with st.expander("Dados Outubro"):
                st.dataframe(df_out, use_container_width=True)
        
        with row4_col2:
            grafico_nov, df_nov = gera_grafico_compacto_mes(11, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_nov, use_container_width=True)
            with st.expander("Dados Novembro"):
                st.dataframe(df_nov, use_container_width=True)
        
        with row4_col3:
            grafico_dez, df_dez = gera_grafico_compacto_mes(12, df_selecionado, ano_selecionado1)
            st.altair_chart(grafico_dez, use_container_width=True)
            with st.expander("Dados Dezembro"):
                st.dataframe(df_dez, use_container_width=True)
        
        # Adicionar um resumo anual abaixo do grid
        st.write("### Resumo Anual")
        
        # Obter dados de todos os meses e combinar
        df_anual = pd.concat([df_jan, df_fev, df_mar, df_abr, df_mai, df_jun, 
                               df_jul, df_ago, df_set, df_out, df_nov, df_dez])
        
        # Agrupar por tipo de atividade para obter o total anual
        df_total_por_tipo = df_anual.groupby('tipo_atividade')['qtd'].sum().reset_index()
        df_total_por_tipo['mes'] = 'Total Anual'
        df_total_por_tipo['ano'] = ano_selecionado1
        
        # Gráfico de resumo anual (maior e mais detalhado)
        grafico_anual = alt.Chart(df_total_por_tipo).mark_bar().encode(
            x=alt.X('tipo_atividade:N', title='Tipo de Atividade'),
            y=alt.Y('qtd:Q', title='Quantidade Total de Atividades'),
            tooltip=['tipo_atividade', 'qtd'],      
            color=alt.Color('tipo_atividade:N', title='Tipo de Atividade')     
        ).properties(
            title=alt.Title(
                text=f'Resumo Anual de Atividades - {ano_selecionado1}'
            ),
            width=800,
            height=400
        ).interactive()
        
        # Exibir gráfico anual e dados
        st.altair_chart(grafico_anual, use_container_width=True)
        
        # Adicionar tabela com dados anuais
        with st.expander("Dados do Resumo Anual"):
            # Adicionar uma linha com o total geral
            total_geral = df_total_por_tipo['qtd'].sum()
            df_total_com_soma = df_total_por_tipo.copy()
            df_total_com_soma.loc[len(df_total_com_soma)] = ['TOTAL', total_geral, 'Total Anual', ano_selecionado1]
            
            st.dataframe(df_total_com_soma, use_container_width=True)
        
    else:
        st.warning("Selecione um ano específico para visualizar o grid mensal de atividades.")
        st.info("Esta funcionalidade não está disponível para a opção 'Todos'.")
# ==============================================================================