# 📊 Projeto de Análise e Visualização de Atestados

## 📌 Sobre o Projeto
Este projeto tem como objetivo a extração, transformação e carregamento (ETL) de dados relacionados a atestados médicos, armazenando essas informações em um banco MySQL para posterior análise e visualização através de um dashboard interativo utilizando Streamlit.

## 🏗 Etapas do Projeto
1. **Extração dos Dados**: Os dados foram obtidos a partir de um arquivo Excel e inseridos no banco de dados MySQL.
2. **Transformação e Limpeza**: Durante o processo de ETL, diversas inconsistências foram corrigidas, incluindo:
   - Conversão de datas para um formato padrão.
   - Remoção de valores inválidos (exemplo: datas inexistentes como `0001-01-01`).
   - Padronização de colunas.
3. **Carga no Banco de Dados**: Os dados tratados foram inseridos no MySQL.
4. **Consultas SQL**: Foram criadas consultas para responder perguntas analíticas sobre os atestados.
5. **Desenvolvimento do Dashboard**: Um dashboard foi construído com Streamlit para exibir visualizações interativas.

## ⚙️ ETL: Extração, Transformação e Carga
O processo de ETL está implementado nos seguintes arquivos:
- `etl.py` e `etl.ipynb`: Contêm a lógica de extração, tratamento e carga dos dados no banco MySQL.
  - No arquivo Jupyter Notebook (`etl.ipynb`), os passos estão mais explicativos e segmentados para melhor compreensão.
- `utils.py`: Contêm funções auxiliares utilizadas durante a ETL.
- A conexão com o banco de dados foi feita utilizando **dotenv**, garantindo que as credenciais do banco não fiquem expostas.

## 🛠 Consultas SQL
Foram realizadas diversas consultas para análise dos dados, incluindo:
- Quantidade de atestados por departamento.
- Total de gastos por departamento, exibindo os maiores e menores gastos.
- Análise de ocorrências por dia da semana e por mês.
- Associação entre líderes e departamentos liderados.

## 📊 Dashboard Interativo
O dashboard foi desenvolvido utilizando **Streamlit** e inclui diversas visualizações interativas:
- Gráficos de barras para gastos por departamento.
- Análise temporal das ocorrências de atestados.
- Filtros dinâmicos para refinar a visualização dos dados.

A estrutura do dashboard está organizada da seguinte forma:
- `app.py`: Arquivo principal do dashboard.
- `pages/`: Pasta contendo outras páginas adicionais do dashboard, organizando melhor as visualizações.

## 📦 Dependências e Execução
O dashboard está disponível no seguinte link: https://desafio-etl-5ms6no9fvrzrkqek8frvnb.streamlit.app/
Caso a página esteja fora do ar, apenas clique no botão disponível para rodá-la novamente

Para rodar o dashboard, algumas dependências foram ajustadas para a versão da cloud do Streamlit. 
Caso queira executar localmente, siga os passos abaixo:

1. Substitua o `requirements.txt` original pelo conteúdo do arquivo `texto.txt`, que contém todas as versões completas das bibliotecas.
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
3. Execute o dashboard com o comando:
   ```sh
   streamlit run app.py
   ```

## 🎯 Conclusão
Este projeto forneceu insights valiosos sobre os atestados médicos, facilitando a tomada de decisão através de um dashboard interativo. Os desafios encontrados durante a ETL foram resolvidos com tratamentos adequados, garantindo dados confiáveis e estruturados para análise.

