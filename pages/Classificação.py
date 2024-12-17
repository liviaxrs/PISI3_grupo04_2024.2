import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# Título da aplicação
st.title("Previsão de Evasão Universitária")

# Carregar o dataset
dados = pd.read_parquet('pisi3_database/predict_dropout.parquet')

# Criar a variável binária 'is_dropout'
dados['evasao'] = dados['Target'].apply(lambda x: 1 if x == 1 else 0)

# Substituir os valores 0 e 1 por 'Não evadiu' e 'Evadido' para ficar mais claro no streamlit
distribuicao_evasao = dados['evasao'].replace({0: 'Não evadiu', 1: 'Evadiu'})

# Exibir a distribuição
st.write("Distribuição de Evasão:")
st.write(distribuicao_evasao.value_counts())


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
dados_processados['evasao'] = dados['evasao']

# Exibir os dados processados
st.write("Dados após processamento:")
st.write(dados_processados.head())

# Criar as variáveis X (independentes) e y (dependente)
x = dados_processados.drop(columns=['evasao'])
y = dados_processados['evasao']

# Dividir os dados em treino e teste
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

# Verificar as dimensões dos dados de treino e teste
st.write("Dados de treinamento e teste:")
st.write(f"Tamanho do conjunto de treino: {x_train.shape}")
st.write(f"Tamanho do conjunto de teste: {x_test.shape}")

# Função para treinar, prever e avaliar modelos
def treinar_e_avaliar_modelo(modelo, x_train, y_train, x_test, y_test, nome_modelo):
    modelo.fit(x_train, y_train)
    y_pred = modelo.predict(x_test)

    st.write(f"### Modelo: {nome_modelo}")
    acuracia = accuracy_score(y_test, y_pred)
    st.write(f"Acurácia do modelo {nome_modelo}:", acuracia)

    matriz_confusao = confusion_matrix(y_test, y_pred)

    # Substituir os valores 0 e 1 pelos nomes "Não evadiu" e "Evadido"
    categorias = ["Não evadiu", "Evadiu"]

    # Visualizar a matriz de confusão com os rótulos ajustados
    st.write(f"Matriz de Confusão Visual do modelo {nome_modelo}:")
    fig, ax = plt.subplots()
    sns.heatmap(matriz_confusao, annot=True, fmt='d', cmap='Blues', 
                xticklabels=categorias, yticklabels=categorias, ax=ax)
    ax.set_xlabel("Predito")
    ax.set_ylabel("Real")
    st.pyplot(fig)

    # Relatório de Classificação sem 'accuracy'
    relatorio_classificacao = classification_report(y_test, y_pred, output_dict=True)
    relatorio_filtrado = {k: v for k, v in relatorio_classificacao.items() if k != 'accuracy'}
    relatorio_renomeado = {
        'Não evadiu' if k == '0' else 'Evadiu' if k == '1' else k: v 
        for k, v in relatorio_filtrado.items()
    }

    # Convertendo em DataFrame e exibindo
    st.write(f"Relatório de Classificação do modelo {nome_modelo}:")
    st.dataframe(pd.DataFrame(relatorio_renomeado).transpose())

# Modelos disponíveis
modelos = {
    "KNN": KNeighborsClassifier(),
    "Random Forest": RandomForestClassifier(class_weight='balanced', random_state=42),
    "SVM": SVC(class_weight='balanced', probability=True, random_state=42)
}

# Adicionar seleção para o modelo
modelo_selecionado = st.selectbox("Escolha o modelo para avaliação:", list(modelos.keys()))

# Executar e avaliar o modelo selecionado
if modelo_selecionado:
    modelo_escolhido = modelos[modelo_selecionado]
    treinar_e_avaliar_modelo(modelo_escolhido, x_train, y_train, x_test, y_test, modelo_selecionado)