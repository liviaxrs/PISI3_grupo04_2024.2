import streamlit as st
import pandas as pd
import plotly.express as px

dados = pd.read_parquet('pisi3_database/dataset_traduzido.parquet')

st.write(dados.head())

# Agrupar variáveis em categorias
grupos_variaveis = {
    "Financeiro": ["Devedor", "Pagamento em dia", "Bolsista"],
    "Família": ["Qualificação da mãe", "Qualificação do pai", "Ocupação da mãe", "Ocupação do pai"],
    "Demografia": ["Gênero", "Estado civil"],
    "Outros": ["Deslocado", "Necessidade de educação especial"]
}

# Adicionar interatividade para selecionar grupos de variáveis
grupo_selecionado = st.selectbox("Escolha o grupo de variáveis para análise:", list(grupos_variaveis.keys()))

variaveis_selecionadas = grupos_variaveis[grupo_selecionado]
for variavel in variaveis_selecionadas:
    if variavel in ["Qualificação da mãe", "Qualificação do pai", "Ocupação da mãe", "Ocupação do pai"]:
        # Manter gráfico existente para estas variáveis
        dados_plot = dados[variavel].copy()
        contagem = dados_plot.value_counts()
        dados_plot = dados_plot.replace(contagem[contagem < 71].index, 'Outro')
        dados_plot = dados_plot.value_counts().reset_index()
        dados_plot.columns = [variavel, 'Contagem']
        dados_plot[variavel] = dados_plot[variavel].apply(lambda x: '<br>'.join(x.split(' ')))
        fig = px.bar(dados_plot, x=variavel, y="Contagem", title=f"Distribuição de {variavel}")
        fig.update_layout(xaxis=dict(tickangle=0))
    else:
        contagem = dados[variavel].value_counts()
        fig = px.bar(contagem, y=contagem.values, x=contagem.index, title=f"Proporção de {variavel}")
        fig.update_layout(height=400, width=800, showlegend=True)
    st.plotly_chart(fig)
