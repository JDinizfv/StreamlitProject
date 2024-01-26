import pandas as pd
import plotly.express as px
import streamlit as st

# ALTERAÇÕES NOS DATAFRAMES

df_hapvida = pd.read_csv('RECLAMEAQUI_HAPVIDA.csv')
df_ibyte = pd.read_csv('RECLAMEAQUI_IBYTE.csv')
df_nagem = pd.read_csv('RECLAMEAQUI_NAGEM.csv')

df_hapvida['TEMPO'] = pd.to_datetime(df_hapvida['TEMPO'])
df_nagem['TEMPO'] = pd.to_datetime(df_nagem['TEMPO'])
df_ibyte['TEMPO'] = pd.to_datetime(df_ibyte['TEMPO'])

df_hapvida['ESTADO'] = df_hapvida['LOCAL'].str.extract(r'\b([A-Z]{2})\b')
df_nagem['ESTADO'] = df_nagem['LOCAL'].str.extract(r'\b([A-Z]{2})\b')
df_ibyte['ESTADO'] = df_ibyte['LOCAL'].str.extract(r'\b([A-Z]{2})\b')



# FUNÇÕES GRÁFICAS

def plot_serie_temporal_plotly(df, date_column, casos_column, title="Série Temporal de Reclamações"):
    
    df = df.copy()
    
    # Converte a coluna de data para o formato datetime
    df[date_column] = pd.to_datetime(df[date_column])

    # Agrupa o DataFrame pela coluna de data e calcula o número de casos em cada data
    serie_temporal = df.groupby(date_column)[casos_column].count().reset_index()

    # Cria o gráfico de série temporal usando Plotly
    fig = px.line(serie_temporal, x=date_column, y=casos_column, 
                  title=title, labels={date_column: 'Data', casos_column: 'Número de Reclamações'})

    # Mostra o gráfico
    return fig

def plot_reclamacoes_por_estado(df, estado_column, title="Frequência de Reclamações por Estado"):
    
    df = df.copy()
    
    # Agrupa o DataFrame pela coluna de estado e calcula o número de reclamações em cada estado
    reclamacoes_por_estado = df[estado_column].value_counts().reset_index()
    reclamacoes_por_estado.columns = ['Estado', 'Frequência']

    # Cria o gráfico de barras usando Plotly
    fig = px.bar(reclamacoes_por_estado, x='Estado', y='Frequência',
                 title=title, labels={'Frequência': 'Número de Reclamações', 'Estado': 'Estado'})
    
    fig.update_layout(xaxis_tickangle=-45)
    
    # Mostra o gráfico
    return fig

def plot_frequencia_status(df, status_column, title="Frequência de Cada Tipo de Status"):
    
    df = df.copy()
    
    # Calcula a frequência de cada tipo de status
    frequencia_status = df[status_column].value_counts().reset_index()
    frequencia_status.columns = ['Status', 'Frequência']

    # Cria o gráfico de barras usando Plotly
    fig = px.bar(frequencia_status, x='Status', y='Frequência',
                 title=title, labels={'Frequência': 'Número de Ocorrências', 'Status': 'Status'})

    # Adiciona inclinação aos rótulos do eixo x
    fig.update_layout(xaxis_tickangle=-45)

    # Mostra o gráfico
    return fig

def plot_distribuicao_tamanho_texto(df, texto_column, title="Distribuição do Tamanho do Texto"):
    
    df = df.copy()
    
    # Calcula o tamanho de cada texto na coluna
    df['Tamanho do Texto'] = df[texto_column].apply(len)

    # Cria o histograma usando Plotly
    fig = px.histogram(df, x='Tamanho do Texto',
                       title=title, labels={'Tamanho do Texto': 'Número de Caracteres'})

    # Adiciona inclinação aos rótulos do eixo x
    fig.update_layout(xaxis_tickangle=-45)

    # Mostra o gráfico
    return fig

# Widgets para seleção
selected_company = st.selectbox("Selecione a empresa", ["Hapvida", "Ibyte", "Nagem"])



# Carrega os dados
if selected_company == "Nagem":
    data = df_nagem
elif selected_company == "Ibyte":
    data = df_ibyte
else:
    data = df_hapvida

selected_state = st.selectbox("Selecione o estado", ['Todos'] + data['ESTADO'].unique().tolist())
selected_status = st.selectbox("Selecione o status", ['Todos'] + data['STATUS'].unique().tolist())
description_length = st.slider("Selecione o tamanho da descrição", 0, 18000, 1000, format="%d")

# Filtrar os dados
if selected_state == 'Todos':
    # Filtrar para todos os estados
    filtered_data = data[(data['STATUS'] == selected_status) & 
                               (data['DESCRICAO'].apply(len) >= description_length)]
elif selected_state == 'Todos' and selected_status == 'Todos':
    # Sem filtros para Estados e Status
    filtered_data = data[(data['DESCRICAO'].apply(len) >= description_length) & data['ESTADO'] & data['STATUS']]

elif selected_status == 'Todos':
    # Filtrar apenas para todos os Status
    filtered_data = data[(data['ESTADO'] == selected_state) & (data['DESCRICAO'].apply(len) >= description_length)]
else:
    # Filtrar para um estado específico
    filtered_data = data[(data['ESTADO'] == selected_state) & 
                               (data['STATUS'] == selected_status) & 
                               (data['DESCRICAO'].apply(len) >= description_length)]





# Apresentar os resultados
st.write("Número de reclamações:", len(filtered_data))

# Cria os gráficos

# Gráfico de série temporal do número de reclamações
st.plotly_chart(plot_serie_temporal_plotly(filtered_data, 'TEMPO', 'ID', f'Série Temporal de Reclamações - {selected_company}'))

# Frequência de reclamações por estado
st.plotly_chart(plot_reclamacoes_por_estado(filtered_data, 'ESTADO', f'Frequência de Reclamações por Estado - {selected_company}'))

# Frequência de cada tipo de **STATUS**
st.plotly_chart(plot_frequencia_status(filtered_data, 'STATUS', f'Frequência de Cada Tipo de Status - {selected_company}'))



# Distribuição do tamanho do texto (coluna **DESCRIÇÃO**)
st.plotly_chart(plot_distribuicao_tamanho_texto(filtered_data, 'DESCRICAO', f'Distribuição do Tamanho do Texto - {selected_company}'))
