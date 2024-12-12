import streamlit as st

# Configurações da página
st.set_page_config(
    page_title="ProAluno",
    layout="wide",
)

st.write("""
    <h2>Sobre o Projeto</h2>
    <p>Nesta análise foi utilizado o dataset disponível no Kaggle: <a href='https://www.kaggle.com/datasets/syedfaizanalii/predict-students-dropout-and-academic-success'>Predict Students Dropout and Academic Success</a>.</p>
""", unsafe_allow_html=True)


st.divider()
st.write("""
        <h2>Perguntas que orientam a análise</h2>
        <p>Para guiar a análise dos dados, foram definidas as seguintes perguntas:</p>
        <h3>Pergunta 1</h3>
        <p>De que forma fatores socioeconômicos, como a ocupação dos pais, a regularidade do pagamento das mensalidades, a condição de endividamento e a concessão de bolsa de estudos, podem ser utilizados para prever a probabilidade de evasão de alunos universitários?</p>
        <h3>Pergunta 2</h3>
        <p>Ao agrupar alunos com base em características acadêmicas, socioeconômicas e de adaptação, quais padrões emergem na formação de grupos e como esses padrões podem ser utilizados para categorizar alunos em diferentes níveis de risco acadêmico?
</p>
""", unsafe_allow_html=True)


