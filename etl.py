import pandas as pd
import mysql.connector
import numpy as np
import dotenv
import os
from utils import corrigir_custo, preencher_departamento

# Ler a planilha ignorando as 14 primeiras linhas (começando da 15)
df = pd.read_excel("Dados_Desafio.xlsx", skiprows=13, engine="openpyxl")

# Renomear colunas
df.columns = ["codigo", "custo", "identificacao", "funcionario", "departamento", "data_atestado", "especialidade", "motivo", "lider"]

# Remover todas as colunas que estão vazias
df.dropna(axis=1, how='all', inplace=True)

# Remover os espaços presentes e transformar valores vazios
df["departamento"] = df["departamento"].astype(str).str.strip()
df["departamento"] = df["departamento"].replace(["", "nan", "None"], np.nan)

# Lógica para preecher departamentos vazios baseando-se nos vizinhos
df = preencher_departamento(df)

# Converter "data_atestado" para formato de data
df["data_atestado"] = pd.to_datetime(df["data_atestado"], dayfirst=True, errors='coerce')

# Tratar a coluna "custo" (remover '--' e transformar em número)
df["custo"] = df["custo"].apply(corrigir_custo)

# Calcular a mediana para cada funcionário e departamento
mediana_custo = df.groupby(["funcionario", "departamento"])["custo"].median()

# Função para verificar valores suspeitos
def corrigir_valores_errados(row):
    funcionario = row["funcionario"]
    departamento = row["departamento"]
    valor = row["custo"]
    
    # Mediana esperada para aquele funcionário/departamento
    mediana_esperada = mediana_custo.get((funcionario, departamento), np.nan)

    # Se o valor for 10x maior ou menor que a mediana, corrigimos
    if not np.isnan(mediana_esperada) and (valor > 10 * mediana_esperada or valor < 0.1 * mediana_esperada):
        return mediana_esperada  # Substitui pelo valor correto

    return valor  # Mantém o valor original

# Aplicar a correção
df["custo"] = df.apply(corrigir_valores_errados, axis=1)

# Preencher valores vazios com "Desconhecido" em colunas de texto
df.fillna({"especialidade": "Desconhecido", "motivo": "Desconhecido"}, inplace=True)

# print(df[df["codigo"] == 1033413])
print(df[df["codigo"] == 1032237])

# Remover linhas sem código
df = df.dropna(subset=["codigo"])

# Parte do banco de dados

# Conectar ao MySQL
dotenv.load_dotenv()
conn = mysql.connector.connect(
    host=os.environ['HOST_DB'],
    user=os.environ['USER_DB'],  
    password=os.environ['PASSWORD_DB'],  
    database=os.environ['DATABASE']
)
cursor = conn.cursor()
print('Conexão estabelecida')

try:
    cursor.execute("DELETE FROM atestados")
    print('Dados excluídos')
    cursor.execute("ALTER TABLE atestados AUTO_INCREMENT = 1")
    print('Auto incremento resetado')

    # Inserir os dados na tabela
    for _, row in df.iterrows():
        sql = """
            INSERT INTO atestados (codigo, custo, funcionario, departamento, data_atestado, especialidade, motivo, lider)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            row["codigo"], row["custo"], row["funcionario"], row["departamento"],
            row["data_atestado"], row["especialidade"], row["motivo"], row["lider"]
        )
        valores = [None if isinstance(v, float) and np.isnan(v) else v for v in valores]
        cursor.execute(sql, valores)
    
    print('Dados novos inseridos')
    conn.commit()

except Exception as e:
    print(f'Erro: {e}')
    conn.rollback()

finally:
    cursor.close()
    conn.close()
    print('Conexão fechada')