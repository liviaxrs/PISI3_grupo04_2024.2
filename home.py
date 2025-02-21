import streamlit as st

import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="ProAluno",
    page_icon="🎓",
    layout="centered",
)



# Título principal
st.markdown("<h1 style='text-align: center; '>📚 ProAluno - Análise da Evasão Universitária</h1>", unsafe_allow_html=True)

st.divider()

# Seção sobre o projeto
st.subheader("📌 Sobre o Projeto")
st.write("Este projeto utiliza dados acadêmicos para prever a evasão de alunos universitários e identificar padrões de sucesso acadêmico.")
st.write("🔗 [Dataset no Kaggle](https://www.kaggle.com/datasets/syedfaizanalii/predict-students-dropout-and-academic-success)")


st.divider()

# Seção de perguntas de pesquisa
st.header("🔍 Perguntas que orientam a análise")

st.subheader("🎯 Pergunta 1")
st.markdown(
    """
    **De que forma fatores socioeconômicos, como a ocupação dos pais, a regularidade do pagamento das mensalidades, 
    a condição de endividamento e a concessão de bolsa de estudos, podem ser utilizados para prever a probabilidade de evasão de alunos universitários?**
    """
)

st.subheader("📌 Pergunta 2")
st.markdown(
    """
    **Ao agrupar alunos com base em características acadêmicas, socioeconômicas e de adaptação, quais padrões emergem na formação de grupos 
    e como esses padrões podem ser utilizados para categorizar alunos em diferentes níveis de risco acadêmico?**
    """
)
