import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE

# Título da aplicação
st.title("Previsão de Evasão Universitária")

# Modelos disponíveis
modelos = {
    "K-Nearest Neighbors (KNN)": KNeighborsClassifier(),
    "Random Forest": RandomForestClassifier(n_estimators=500, max_depth=10, random_state=42, class_weight="balanced"),
    "Support Vector Machine (SVM)": SVC(class_weight='balanced', probability=True, random_state=42)
}

# Adicionar seleção para o modelo
modelo_selecionado = st.selectbox("Escolha o modelo para avaliação:", list(modelos.keys()))

# Carregar o dataset
dados = pd.read_parquet('pisi3_database/predict_dropout.parquet')




# Substituir os valores 0 e 1 por 'Não evadiu' e 'Evadido' para ficar mais claro no streamlit
#distribuicao_evasao = dados['Target'].replace({0: 'Não evadiu', 1: 'Evadiu'})
#st.write("Distribuição de Evasão:")
#st.write(distribuicao_evasao.value_counts())

# Substituir os valores 0 e 1 por 'Não evadiu' e 'Evadido' para ficar mais claro no streamlit
distribuicao_evasao = dados['Target'].replace({2: 'Não evadiu', 1: 'Evadiu', 3: 'Graduando'}).value_counts().reset_index()
# Exibir a distribuição
st.write("Distribuição de Evasão:")
fig = px.bar(distribuicao_evasao, x='Target', y='count',  
             title='Distribuição de Evasão')
fig.update_traces(textposition='outside')
fig.update_layout(xaxis_title='Status do Aluno', yaxis_title='Quantidade de Alunos')
st.plotly_chart(fig)

# Preparando a coluna 'Target'
dados.drop(dados[dados['Target'] == 3].index, inplace=True)
dados['Target'] = dados['Target'].apply(lambda x: 1 if x == 1 else 0)
dados = dados.reset_index(drop=True)


# Selecionar as variáveis independentes categóricas e numéricas
variaveis_categoricas = ["Mother's occupation", "Father's occupation"]
variaveis_binarias = ['Tuition fees up to date', 'Scholarship holder', 'Debtor']  # Variáveis binárias

# Aplicar o One-Hot Encoding para as variáveis categóricas
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded_categoricas = encoder.fit_transform(dados[variaveis_categoricas])

# Criar um DataFrame para os dados categóricos codificados
encoded_categoricas_df = pd.DataFrame(encoded_categoricas, columns=encoder.get_feature_names_out(variaveis_categoricas))

# Dados binários
binarias_df = dados[variaveis_binarias]

# Combinar todas as variáveis independentes processadas
dados_processados = pd.concat([encoded_categoricas_df, binarias_df], axis=1)

# Adicionar a variável dependente (evasão) ao conjunto processado
dados_processados['Target'] = dados['Target']

# Exibir os dados processados
st.write("Dados após processamento:")
st.write(dados_processados.head())

# Criar as variáveis X (independentes) e y (dependente)
x = dados_processados.drop(columns=['Target'])
y = dados_processados['Target']

# Dividir os dados em treino e teste
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)


# Verificar as dimensões dos dados de treino e teste
st.write("Dados de treinamento e teste:")
st.write(f"Tamanho do conjunto de treino: {x_train.shape}")
st.write(f"Tamanho do conjunto de teste: {x_test.shape}")

# Função para treinar, prever e avaliar modelos
def treinar_e_avaliar_modelo(modelo, x_train, y_train, x_test, y_test, nome_modelo):

    st.write(f"### Modelo Escolhido: {nome_modelo}")
    
    if nome_modelo == 'Support Vector Machine (SVM)':
        modelo.fit(x_train, y_train)
        y_pred = modelo.predict(x_test)
        y_train_pred = modelo.predict(x_train)
    else:
        # Aplicar balanceamento somente nos modelos 'RF' e 'KNN':
        smote = SMOTE(sampling_strategy="auto", random_state=42)
        x_train, y_train = smote.fit_resample(x_train, y_train)

        modelo.fit(x_train, y_train)
        y_pred = modelo.predict(x_test)
        y_train_pred = modelo.predict(x_train)


    # Visualizar a matriz de confusão com os rótulos ajustados
    st.write(f"Matriz de Confusão:")
    c1,_,c2,_,c3 = st.columns([.3,.05,.35,.05,.25])
    matriz_confusao = confusion_matrix(y_test, y_pred)
    categorias = ["Não evadiu", "Evadiu"]
    fig, ax = plt.subplots()
    sns.heatmap(matriz_confusao, annot=True, fmt='d', ax=ax, cmap='Blues', cbar=False)
    ax.set_xlabel('Valores Previstos')
    ax.set_ylabel('Valores Reais')
    ax.xaxis.set_ticklabels(categorias)
    ax.yaxis.set_ticklabels(categorias)
    c1.pyplot(fig)

    # Relatório de Classificação - TESTE
    relatorio_classificacao_teste = classification_report(y_test, y_pred, output_dict=True)
    relatorio_filtrado_teste = {k: v for k, v in relatorio_classificacao_teste.items() if k != 'accuracy'}
    relatorio_renomeado_teste = {
        'Não evadiu' if k == '0' else 'Evadiu' if k == '1' else k: v 
        for k, v in relatorio_filtrado_teste.items()
    }
    # Relatório de Classificação - TREINO
    relatorio_classificacao_treino = classification_report(y_train, y_train_pred, output_dict=True)
    relatorio_filtrado_treino = {k: v for k, v in relatorio_classificacao_treino.items() if k != 'accuracy'}
    relatorio_renomeado_treino = {
        'Não evadiu' if k == '0' else 'Evadiu' if k == '1' else k: v 
        for k, v in relatorio_filtrado_treino.items()
    }
    # Exibição dos relatorios no Streamlit
    c2.write(f"Relatórios de Classificação TESTE:")
    acuracia = accuracy_score(y_test, y_pred)
    c2.write(f"Acurácia: {acuracia:.2f}")
    c2.dataframe(pd.DataFrame(relatorio_renomeado_teste).transpose())
    c3.write(f"Relatórios de Classificação TREINO:")
    acuracia_treino = accuracy_score(y_train, y_train_pred)
    c3.write(f"Acurácia: {acuracia_treino:.2f}")
    c3.dataframe(pd.DataFrame(relatorio_renomeado_treino).transpose())

# Executar e avaliar o modelo selecionado
if modelo_selecionado:
    modelo_escolhido = modelos[modelo_selecionado]
    treinar_e_avaliar_modelo(modelo_escolhido, x_train, y_train, x_test, y_test, modelo_selecionado)