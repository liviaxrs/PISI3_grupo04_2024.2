import pandas as pd
import streamlit as st
import plotly.express as px


st.title("Analise exploratoria inicial")
st.write("Este streamlit tem como objetivo exibir a analise exploratoria inicial do dataset 'Predict Students Dropout and Academic Success'")

def load_data():
    data = pd.read_csv('pisi3_database/dataset_mapeado.csv', delimiter=',')
    return data

st.subheader('Raw data:')
dataset=load_data()
dataset.drop(columns=['Unnamed: 0'], inplace=True)
st.write(dataset)

st.subheader('Analise de variaveis categoricas: ')
columns = dataset.columns.tolist()
coluna_selecionada = st.selectbox('Escolha uma coluna', columns, placeholder='Escolha uma coluna:')
if coluna_selecionada:
    graph = px.pie(dataset, names=coluna_selecionada,
                title=f'Proporção por {coluna_selecionada}',
                hole=0.4)
    st.plotly_chart(graph, use_container_width=True)
