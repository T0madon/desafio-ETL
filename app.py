import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados do arquivo CSV
@st.cache_data
def get_data():
    try:
        df = pd.read_csv('dados_dashboard.csv')
        # Converter colunas de data se necessário
        if 'data_atestado' in df.columns:
            df['data_atestado'] = pd.to_datetime(df['data_atestado'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("Arquivo 'dados_dashboard.csv' não encontrado.")
        return pd.DataFrame()

# DASHBOARD
df = get_data()
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

    # Métricas de custo
    custo_total = df['custo'].sum().round(2)
    custo_gerentes = df[df['departamento'] == 'Gerente']['custo'].sum().round(2)
    
    col_metric1, col_metric2 = st.columns(2)
    with col_metric1:
        st.metric("Custo Total com Atestados", f"R$ {custo_total:,.2f}")
    with col_metric2:
        st.metric("Custo com Gerentes", f"R$ {custo_gerentes:,.2f}")

    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de gastos por departamento
        gastos = df.groupby('departamento')['custo'].sum().reset_index()
        gastos = gastos.rename(columns={'custo': 'total_gasto'})
        gastos = gastos.sort_values('total_gasto', ascending=False)
        
        gastos['total_gasto'] = gastos['total_gasto'].round(2)
        gastos_menores = gastos.sort_values('total_gasto').head(10)

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
        
        if 'data_atestado' in df.columns:
            ocorrencias = df[df['data_atestado'].notna()].copy()
            ocorrencias['dia_semana'] = ocorrencias['data_atestado'].dt.day_name()
            ocorrencias = ocorrencias.groupby('dia_semana').size().reset_index(name='total')
            
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

        if 'data_atestado' in df.columns:
            ocorrencias_mensais = df[df['data_atestado'].notna()].copy()
            ocorrencias_mensais['data'] = ocorrencias_mensais['data_atestado'].dt.strftime('%m/%y')
            ocorrencias_mensais = ocorrencias_mensais.groupby('data').size().reset_index(name='total_mensal')

            # Calcular acumulado
            ocorrencias_mensais = ocorrencias_mensais.sort_values('data')
            ocorrencias_mensais['acumulado'] = ocorrencias_mensais['total_mensal'].cumsum()

        if not ocorrencias_mensais.empty:
            fig = px.bar(
                ocorrencias_mensais,
                x='data',
                y='acumulado',
                text='acumulado',
                title='Ocorrências Acumuladas por Mês',
                labels={'data': 'Mês/Ano', 'acumulado': 'Total Acumulado'},
            )
            
            fig.update_xaxes(categoryorder='category ascending')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhum dado encontrado para exibição.")

with aba3:
    st.write("Visualizações específicas por funcionário")
    
    # Gráfico Top 10 funcionários com mais atestados (quantidade)
    if 'funcionario' in df.columns:
        atestados_por_funcionario = df['funcionario'].value_counts().reset_index()
        atestados_por_funcionario.columns = ['funcionario', 'total_atestados']
            
        st.plotly_chart(
            px.bar(
                atestados_por_funcionario.head(10),
                x='funcionario',
                y='total_atestados',
                text='total_atestados',
                title='Top 10 - Quantidade de Atestados',
                labels={'funcionario': 'Funcionário', 'total_atestados': 'N° de Atestados'},
                color_discrete_sequence=['#636EFA']
            ).update_traces(textposition='outside'),
            use_container_width=True
        )
    
    # Gráfico Top 10 funcionários que mais custaram (valor total)
    if all(col in df.columns for col in ['funcionario', 'custo']):
        custo_por_funcionario = df.groupby('funcionario')['custo'].sum().reset_index()
        custo_por_funcionario = custo_por_funcionario.rename(columns={'custo': 'total_gasto'})
        custo_por_funcionario['total_gasto'] = custo_por_funcionario['total_gasto'].round(2)
        custo_por_funcionario = custo_por_funcionario.sort_values('total_gasto', ascending=False)
            
        st.plotly_chart(
            px.bar(
                custo_por_funcionario.head(10),
                x='funcionario',
                y='total_gasto',
                text='total_gasto',
                title='Top 10 - Maiores Custos com Atestados (R$)',
                labels={'funcionario': 'Funcionário', 'total_gasto': 'Valor Total'},
                color_discrete_sequence=['#EF553B'],
                text_auto='.2f'
            ).update_traces(textposition='outside'),
            use_container_width=True
        )
