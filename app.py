import streamlit as st
import pandas as pd
import mysql.connector
import plotly.graph_objects as go
import plotly.express as px

import os
import dotenv

# Conectar ao MySQL
def get_data(query):
    dotenv.load_dotenv()
    conn = mysql.connector.connect(
        host=os.environ['HOST_DB'],
        user=os.environ['USER_DB'],  
        password=os.environ['PASSWORD_DB'],  
        database=os.environ['DATABASE']
    )
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# DASHBOARD
df = get_data('SELECT * FROM atestados')

# print(df)

st.set_page_config(layout='wide')
st.title("Dashboard de Atestados Médicos")

st.sidebar.title('Filtro de Funcionários')

filtro_funcionario = st.sidebar.multiselect(
    'Funcionários',
    df['funcionario'].unique()
)

if filtro_funcionario:
    df = df[df['funcionario'].isin(filtro_funcionario)]

aba1, aba2, aba3 = st.tabs(['Dataset', 'Custos', 'Funcionários'])

with aba1:
    st.dataframe(df)

with aba2:

    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de gastos por departamento
        gastos = get_data("SELECT departamento, SUM(custo) AS total_gasto FROM atestados GROUP BY departamento ORDER BY total_gasto DESC")

        gastos_menores = get_data("""
            SELECT departamento, SUM(custo) AS total_gasto
            FROM atestados
            GROUP BY departamento
            ORDER BY total_gasto ASC
            LIMIT 10;
        """)

        if not gastos_menores.empty:
            st.plotly_chart(
            px.bar(
                gastos.head(10),
                x='total_gasto',
                y='departamento',
                range_x=(0, gastos.max()),
                text='total_gasto',
                title='Top 10 Departamentos com Maiores Gastos'
            ),
            use_container_width=True
        )
        else:
            st.warning("Nenhum dado encontrado para os menores gastos.")

        if not gastos_menores.empty:
            st.plotly_chart(
                px.bar(
                    gastos_menores,
                    x='total_gasto',
                    y='departamento',
                    range_x=(0, gastos_menores['total_gasto'].max()),
                    text='total_gasto',
                    title='Top 10 Departamentos com Menores Gastos',
                    orientation='h'
                ),
                use_container_width=True
            )
        else:
            st.warning("Nenhum dado encontrado para os menores gastos.")

    with col2:

        dias_traduzidos = {
            "Monday": "Segunda",
            "Tuesday": "Terça",
            "Wednesday": "Quarta",
            "Thursday": "Quinta",
            "Friday": "Sexta",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }
        ordem_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        
        # Ocorrências por dia da semana, tradução e ordenação
        ocorrencias = get_data("""
            SELECT DAYNAME(data_atestado) AS dia_semana, COUNT(*) AS total 
            FROM atestados 
            WHERE data_atestado <> '0001-01-01'
            GROUP BY dia_semana
        """)
        
        ocorrencias["dia_semana"] = ocorrencias["dia_semana"].map(dias_traduzidos)
        ocorrencias["dia_semana"] = pd.Categorical(ocorrencias["dia_semana"], categories=ordem_dias, ordered=True)
        ocorrencias = ocorrencias.sort_values("dia_semana")

        st.plotly_chart(
            px.bar(
                ocorrencias,
                x='dia_semana',
                y='total',
                range_y=(0, ocorrencias.max()),
                text='total',
                title='Ocorrências por dia da semana',
                color_discrete_sequence=['#007BFF'],
            ).update_traces(textposition="outside"),
            use_container_width=True
        )

        # Consulta SQL para obter os dados de ocorrências acumuladas por mês
        ocorrencias_mensais = get_data("""
            WITH ocorrencias_mensais AS (
                SELECT 
                    DATE_FORMAT(data_atestado, '%m/%y') AS data,
                    COUNT(*) AS total_mensal
                FROM atestados
                WHERE data_atestado <> '0001-01-01'
                GROUP BY data
            )
            SELECT 
                o1.data,
                SUM(o2.total_mensal) AS acumulado
            FROM ocorrencias_mensais o1
            JOIN ocorrencias_mensais o2
                ON o1.data >= o2.data
            GROUP BY o1.data
            ORDER BY STR_TO_DATE(o1.data, '%m/%y') ASC;
        """)

        # Verifica se há dados antes de exibir o gráfico
        if not ocorrencias_mensais.empty:
            fig = px.bar(
                ocorrencias_mensais,
                x='data',
                y='acumulado',
                text='acumulado',
                title='Ocorrências Acumuladas por Mês',
                labels={'data': 'Mês/Ano', 'acumulado': 'Total Acumulado'},
                color_discrete_sequence=['#007BFF'],  # Azul para destacar os dados
            )
            
            fig.update_xaxes(categoryorder='category ascending')
            # Exibe o gráfico
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum dado encontrado para exibição.")
