import streamlit as st
import pandas as pd
import plotly.express as px

dados = pd.read_parquet('pisi3_database/dataset_traduzido.parquet')

# Mostrar o dataset
st.write("### Visualização do Dataset")
st.dataframe(dados)

# Agrupar variáveis em categorias
grupos_variaveis = {
    "Financeiro": ["Devedor", "Pagamento em dia", "Bolsista"],
    "Família": ["Qualificação da mãe", "Qualificação do pai"],
    "Demografia": ["Gênero", "Estado civil"],
    "Outros": ["Deslocado", "Necessidade de educação especial"]
}

# Seleção do grupo de variáveis
grupo_selecionado = st.selectbox("Escolha o grupo de variáveis para análise:", list(grupos_variaveis.keys()))
variaveis_selecionadas = grupos_variaveis[grupo_selecionado]

# Função para aplicar filtro para "Outro" em variáveis gerais
def aplicar_filtro(dados_plot):
    contagem = dados_plot.value_counts()
    dados_plot = dados_plot.replace(contagem[contagem < 71].index, 'Outro')
    return dados_plot

# Função para aplicar filtro específico na variável "Necessidade de educação especial"
def aplicar_filtro_necessidade_educacao(dados_plot):
    # Mantém apenas "Sim" e "Não", e substitui os outros valores por "Outro"
    valores_permitidos = ['Sim', 'Não']
    dados_plot = dados_plot.apply(lambda x: x if x in valores_permitidos else 'Outro')
    return dados_plot

# Gráficos de Barra
st.write("### Gráficos de Barra - Visualização Padrão")
# Exibe gráficos de barra para todas as variáveis do grupo selecionado
for variavel in variaveis_selecionadas:
    dados_plot = dados[variavel].copy()
    
    # Aplica filtro somente se a variável não for "Necessidade de educação especial"
    if variavel == "Necessidade de educação especial":
        dados_plot = aplicar_filtro_necessidade_educacao(dados_plot)
    else:
        dados_plot = aplicar_filtro(dados_plot)  # Aplica o filtro para outras variáveis
    
    dados_plot = dados_plot.value_counts().reset_index()
    dados_plot.columns = [variavel, 'Contagem']

    # Se for "Qualificação da mãe" ou "Qualificação do pai", barras horizontais
    if variavel in ["Qualificação da mãe", "Qualificação do pai"]:
        fig = px.bar(dados_plot, 
                     y=variavel, 
                     x="Contagem", 
                     title=f"Distribuição de {variavel}", 
                     orientation='h')  # Barras horizontais
        fig.update_layout(yaxis=dict(tickangle=0, tickmode="linear"))
    else:
        fig = px.bar(dados_plot, 
                     x=variavel, 
                     y="Contagem", 
                     title=f"Distribuição de {variavel}", 
                     orientation='v')  # Barras verticais
        fig.update_layout(xaxis=dict(tickangle=0, tickmode="linear"))
    
    st.plotly_chart(fig)

# Gráficos de comparação com "Target"
st.write("### Comparação com a variável 'Target' - Visualização Padrão")
for variavel in variaveis_selecionadas:
    dados_plot = dados[[variavel, "Target"]].copy()
    
    # Aplica filtro somente se a variável não for "Necessidade de educação especial"
    if variavel == "Necessidade de educação especial":
        dados_plot[variavel] = aplicar_filtro_necessidade_educacao(dados_plot[variavel])
    else:
        dados_plot[variavel] = aplicar_filtro(dados_plot[variavel])  # Aplica o filtro para outras variáveis
    
    # Agrupar por variável e Target para contar as ocorrências
    dados_plot = dados_plot.groupby([variavel, 'Target']).size().reset_index(name='Contagem')

    # Se for "Qualificação da mãe" ou "Qualificação do pai", barras horizontais
    if variavel in ["Qualificação da mãe", "Qualificação do pai"]:
        fig = px.bar(dados_plot, 
                     y=variavel, 
                     x="Contagem", 
                     color='Target', 
                     title=f"Distribuição de {variavel} com Target", 
                     orientation='h')  # Barras horizontais
        fig.update_layout(yaxis=dict(tickangle=0, tickmode="linear"))
    else:
        fig = px.bar(dados_plot, 
                     x=variavel, 
                     y="Contagem", 
                     color='Target', 
                     title=f"Distribuição de {variavel} com Target", 
                     orientation='v')  # Barras verticais
        fig.update_layout(xaxis=dict(tickangle=0, tickmode="linear"))
    
    st.plotly_chart(fig)