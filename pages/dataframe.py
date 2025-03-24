import streamlit as st
import pandas as pd
import time
from app import df

st.title('Tabela Geral')

with st.expander('Colunas'):
    colunas_removidas = ['departamento', 'custo', 'data_atestado']
    colunas_disponiveis = [col for col in df.columns if col not in colunas_removidas]

    colunas = st.multiselect(
        'Selecione as colunas',
        colunas_disponiveis,
        colunas_disponiveis
    )

st.sidebar.title('Filtros')

with st.sidebar.expander('Departamento'):
    departamento_sel = st.multiselect(
        'Selecione o(s) departamento(s)',
        df['departamento'].unique(),
        df['departamento'].unique()
    )

custo_min = df['custo'].min()
custo_max = df['custo'].max()

with st.sidebar.expander('Custo'):
    custo_sel = st.slider(
        'Selecione o custo',
        custo_min, custo_max,
        (custo_min, custo_max)
    )

df['data_atestado'] = pd.to_datetime(df['data_atestado'], errors='coerce')
df_datas_validas = df[df['data_atestado'] > "0100-01-01"]
min_data = df_datas_validas['data_atestado'].min()
max_data = df_datas_validas['data_atestado'].max()

with st.sidebar.expander('Data do Atestado'):
    data_sel = st.date_input(
        'Selecione a Data',
        (min_data, max_data),
        min_value=min_data,
        max_value=max_data
        )
    
query = """
    `departamento` in @departamento_sel and \
    @custo_sel[0] <= custo <= @custo_sel[1] and \
    @data_sel[0] <= `data_atestado` <= @data_sel[1]
"""

filtro = df.query(query)
filtro = filtro[['departamento', 'custo', 'data_atestado'] + colunas]
filtro['data_atestado'] = filtro['data_atestado'].dt.strftime('%d/%m/%Y')

if departamento_sel and custo_sel and data_sel and \
   (not filtro.empty):
    st.dataframe(filtro)
else:
    st.warning("Selecione os filtros que incluam os dados requeridos.")


st.markdown('Escreva o nome do arquivo:')

@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def mensagem_sucesso():
    success = st.success('Download feito com sucesso!')
    time.sleep(2)
    success.empty()

col1, col2 = st.columns(2)
with col1:
    nome_arquivo = st.text_input(
        '',
        label_visibility='collapsed',
    )
    nome_arquivo += '.csv'

with col2:
    st.download_button(
        'Baixar arquivo',
        data=convert_csv(filtro),
        file_name= nome_arquivo,
        mime='text/csv',
        on_click=mensagem_sucesso
    )