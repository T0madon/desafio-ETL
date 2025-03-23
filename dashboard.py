import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
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
# df = get_data('SELECT * FROM atestados')

# print(df)

st.title("Dashboard de Atestados Médicos")

# Filtro por departamento
departamentos = get_data("SELECT DISTINCT departamento FROM atestados")
selected_depto = st.selectbox("Escolha um departamento:", ["Todos"] + list(departamentos["departamento"]))

# Dados principais
query = "SELECT * FROM atestados"
if selected_depto != "Todos":
    query += f" WHERE departamento = '{selected_depto}'"
df = get_data(query)
st.write(df)

# Gráfico de gastos por departamento
st.subheader("Gastos por Departamento")
gastos = get_data("SELECT departamento, SUM(custo) AS total_gasto FROM atestados GROUP BY departamento ORDER BY total_gasto DESC")
fig, ax = plt.subplots()
sns.barplot(x="total_gasto", y="departamento", data=gastos, ax=ax)
st.pyplot(fig)

# Ocorrências por dia da semana
st.subheader("Ocorrências por Dia da Semana")
ocorrencias = get_data("SELECT DAYNAME(data_atestado) AS dia_semana, COUNT(*) AS total FROM atestados GROUP BY dia_semana")
fig, ax = plt.subplots()
sns.barplot(x="dia_semana", y="total", data=ocorrencias, ax=ax)
st.pyplot(fig)