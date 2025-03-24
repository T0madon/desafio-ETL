import pandas as pd
import numpy as np

# Função para corrigir os valores da coluna "Custo do afastamento"
def corrigir_custo(valor):
    if pd.isna(valor) or valor == "--":
        return None 
    try:
        return float(str(valor).replace(",", "."))  
    except ValueError:
        return None  
    
# Função para preencher o departamento verificando apenas as linhas vizinhas
def preencher_departamento(df):
    for idx in range(len(df)):
        if pd.isna(df.at[idx, "departamento"]) or df.at[idx, "departamento"] == "":
            # Olha para a linha acima, se existir
            if idx > 0 and df.at[idx, "funcionario"] == df.at[idx - 1, "funcionario"]:
                df.at[idx, "departamento"] = df.at[idx - 1, "departamento"]
            # Verificar a linha abaixo, se existir
            elif idx < len(df) - 1 and df.at[idx, "funcionario"] == df.at[idx + 1, "funcionario"]:
                df.at[idx, "departamento"] = df.at[idx + 1, "departamento"]
            # Se não encontrar, mantém "DESCONHECIDO"
            else:
                df.at[idx, "departamento"] = "DESCONHECIDO"
    return df