import pandas as pd
import streamlit as st
import plotly.express as px

st.write('Predict Students Dropout and Academic Success')

def load_data():
    data = pd.read_csv('pisi3_database/predict_dropout.csv', delimiter=';')
    return data

st.subheader('Raw data:')
dataset=load_data()
st.write(dataset)

