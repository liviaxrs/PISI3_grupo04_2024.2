import streamlit as st
import pandas as pd
import numpy as np
import pickle
import shap

import matplotlib.pyplot as plt

st.set_page_config(page_title="Previsão de Evasão Universitária", page_icon="🎓", layout="centered")
st.markdown("<h1 style='text-align: center; '>🎓 Previsão de Evasão Universitária</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Este aplicativo prevê se um aluno tem tendência a abandonar a universidade, com base em fatores socioeconômicos.</p>", unsafe_allow_html=True)
st.divider()

# Carregar modelo
with open("pages/randomforest.pkl", "rb") as file:
    model = pickle.load(file)

# Opções para ocupações dos pais

ocupacoes_mae = {
    "Ensino Secundário - 12.º Ano de Escolaridade ou Eq.": "Mother's qualification_1",
    "Ensino Superior - Licenciatura ": "Mother's qualification_2",
    "Ensino básico 1º ciclo (4º/5º ano) ou equiv.": "Mother's qualification_37",
    "Ensino Básico 3º Ciclo (9º/10º/11º Ano) ou Equiv. ": "Mother's qualification_19",
    "Ensino Básico 2.º Ciclo (6.º/7.º/8.º Ano) ou Equiv.": "Mother's qualification_38",
    "Ensino Superior - Bacharelado ": "Mother's qualification_3",
    "Outro": "Mother's qualification_200",
    "Desconhecido": "Mother's qualification_34"
}
ocupacoes_pai = {
    "Ensino Secundário - 12.º Ano de Escolaridade ou Eq.": "Father's qualification_1",
    "Ensino básico 1º ciclo (4º/5º ano) ou equiv.": "Father's qualification_37",
    "Ensino Básico 3º Ciclo (9º/10º/11º Ano) ou Equiv. ": "Father's qualification_19",
    "Ensino Básico 2.º Ciclo (6.º/7.º/8.º Ano) ou Equiv.": "Father's qualification_38",
    "Ensino Superior - Bacharelado": "Father's qualification_3",
    "Outro": "Father's qualification_200",
    "Desconhecido": "Father's qualification_34"
}

# Criar inputs no Streamlit
mother_occupation = st.selectbox("📖 Qualificação da Mãe", list(ocupacoes_mae.keys()))
father_occupation = st.selectbox("📖 Qualificação do pai", list(ocupacoes_pai.keys()))
tuition_fees = st.radio("💰 Mensalidade em dia?", ["Sim", "Não"],horizontal=True)
scholarship_holder = st.radio("🎓 Bolsista?", ["Sim", "Não"],horizontal=True)
debtor = st.radio("🚨 Está devendo alguma mensalidade?", ["Sim", "Não"],horizontal=True)

st.divider()

# Converter valores para numéricos
tuition_fees = 1 if tuition_fees == "Sim" else 0
scholarship_holder = 1 if scholarship_holder == "Sim" else 0
debtor = 1 if debtor == "Sim" else 0

qualification_mother = ocupacoes_mae[mother_occupation]
qualification_father = ocupacoes_pai[father_occupation]

# Criar DataFrame para entrada do modelo
input_data = pd.DataFrame({
    "Mother's qualification_1": [1 if qualification_mother == "Mother's qualification_1" else 0],
    "Mother's qualification_2": [1 if qualification_mother == "Mother's qualification_2" else 0],
    "Mother's qualification_37": [1 if qualification_mother == "Mother's qualification_37" else 0],
    "Mother's qualification_19": [1 if qualification_mother == "Mother's qualification_19" else 0],
    "Mother's qualification_38": [1 if qualification_mother == "Mother's qualification_38" else 0],
    "Mother's qualification_3": [1 if qualification_mother == "Mother's qualification_3" else 0],
    "Mother's qualification_200": [1 if qualification_mother == "Mother's qualification_200" else 0],
    "Mother's qualification_34": [1 if qualification_mother == "Mother's qualification_34" else 0],
    "Father's qualification_1": [1 if qualification_father == "Father's qualification_1" else 0],
    "Father's qualification_37": [1 if qualification_father == "Father's qualification_37" else 0],
    "Father's qualification_19": [1 if qualification_father == "Father's qualification_19" else 0],
    "Father's qualification_38": [1 if qualification_father == "Father's qualification_38" else 0],
    "Father's qualification_3": [1 if qualification_father == "Father's qualification_3" else 0],
    "Father's qualification_200": [1 if qualification_father == "Father's qualification_200" else 0],
    "Father's qualification_34": [1 if qualification_father == "Father's qualification_34" else 0],
    "Tuition fees up to date": [tuition_fees],
    "Scholarship holder": [scholarship_holder],
    "Debtor": [debtor]
})

# **3. Aplicar One-Hot Encoding**
# O modelo foi treinado com One-Hot Encoding, então precisamos transformar os inputs da mesma forma.
# Suponha que você tenha salvo as colunas do treino original:

with open("pages/columns.pkl", "rb") as file:
    feature_columns = pickle.load(file)


# Garantir que as colunas do input estejam no mesmo formato do treino
for col in feature_columns:
    if col not in input_data:
        input_data[col] = 0  # Adiciona colunas ausentes com valor 0

# Reordenar as colunas para bater com o modelo
input_data = input_data[feature_columns]
#st.table(input_data)

if st.button("🔍 Fazer Previsão", use_container_width=True):
    prediction = model.predict(input_data)
    result = "🚀 O aluno tem tendência a continuar na universidade!" if prediction[0] == 0 else "⚠️ O aluno pode estar em risco de evasão."
    st.markdown(f"<h3 style='text-align: center; '>{result}</h3>", unsafe_allow_html=True)

# grafico SHAP
explainer = shap.Explainer(model)
shap_values = explainer(input_data)

st.write("### Gráfico de Força SHAP")
shap.initjs()
shap_html = shap.plots.force(explainer.expected_value, shap_values.values, input_data.iloc[0, :])
st.components.v1.html(shap_html, height=300)