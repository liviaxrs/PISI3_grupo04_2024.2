import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Previsão de Evasão Universitária", page_icon="🎓", layout="centered")
st.markdown("<h1 style='text-align: center; '>🎓 Previsão de Evasão Universitária</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Este aplicativo prevê se um aluno tem tendência a abandonar a universidade, com base em fatores socioeconômicos.</p>", unsafe_allow_html=True)

tab1, tab2= st.tabs(["Previsão","Sobre o modelo"])
with open("pages/randomforest.pkl", "rb") as file:
    model = pickle.load(file)
with open("pages/columns.pkl", "rb") as file:
    feature_columns = pickle.load(file)

with tab1:
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

    mother_occupation = st.selectbox("📖 Qualificação da Mãe", list(ocupacoes_mae.keys()))
    father_occupation = st.selectbox("📖 Qualificação do pai", list(ocupacoes_pai.keys()))
    tuition_fees = st.radio("🚨 A mensalidade está em dia?", ["Sim", "Não"],horizontal=True)
    scholarship_holder = st.radio("🎓 Bolsista?", ["Sim", "Não"],horizontal=True)
    debtor = st.radio("💰 É devedor?", ["Sim", "Não"],horizontal=True)

    st.divider()

    tuition_fees = 1 if tuition_fees == "Sim" else 0
    scholarship_holder = 1 if scholarship_holder == "Sim" else 0
    debtor = 1 if debtor == "Sim" else 0

    qualification_mother = ocupacoes_mae[mother_occupation]
    qualification_father = ocupacoes_pai[father_occupation]

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


    for col in feature_columns:
        if col not in input_data:
            input_data[col] = 0  

    input_data = input_data[feature_columns]

    if st.button("🔍 Fazer Previsão", use_container_width=True):
        prediction = model.predict(input_data)
        result = "🚀 O aluno tem tendência a continuar na universidade!" if prediction[0] == 0 else "⚠️ O aluno pode estar em risco de evasão."
        st.markdown(f"<h3 style='text-align: center; '>{result}</h3>", unsafe_allow_html=True)

with tab2:
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
    from imblearn.over_sampling import SMOTE
    modelos = {
    "K-Nearest Neighbors (KNN)": KNeighborsClassifier(),
    "Random Forest": RandomForestClassifier(n_estimators=500, max_depth=10, random_state=42, class_weight="balanced"),
    "Support Vector Machine (SVM)": SVC(class_weight='balanced', probability=True, random_state=42)
}

    # Adicionar seleção para o modelo
    modelo_selecionado = st.selectbox("Escolha o modelo para avaliação:", list(modelos.keys()))

    # Carregar o dataset
    dados = pd.read_parquet('pisi3_database/predict_dropout.parquet')


    # Preparando a coluna 'Target'
    dados.drop(dados[dados['Target'] == 3].index, inplace=True)
    dados['Target'] = dados['Target'].apply(lambda x: 1 if x == 1 else 0)
    dados = dados.reset_index(drop=True)

    # selecionando variaveis categoricas e binarias
    variaveis_categoricas = ["Mother's qualification", "Father's qualification"]
    variaveis_binarias = ['Tuition fees up to date', 'Scholarship holder', 'Debtor']

    columns = ["Mother's qualification", "Father's qualification"]

    #Agrupando valores com baixa frequência em uma categoria "200"
    for column in columns:
        plot_data = dados[column].copy()
        value_counts = plot_data.value_counts()
        dados[column] = dados[column].replace(value_counts[value_counts < 50].index, 200)

    #aplicando one-hot encoding
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_categoricas = encoder.fit_transform(dados[variaveis_categoricas])
    encoded_categoricas_df = pd.DataFrame(encoded_categoricas, columns=encoder.get_feature_names_out(variaveis_categoricas))

    binarias_df = dados[variaveis_binarias]

    # Combinar todas as variáveis independentes processadas
    dados_processados = pd.concat([encoded_categoricas_df, binarias_df], axis=1)

    # Adicionar a variável target ao conjunto ja processado
    dados_processados['Target'] = dados['Target']


    # Dividir os dados em treino e teste
    x = dados_processados.drop(columns=['Target'])
    y = dados_processados['Target']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

    # Função para treinar, prever e avaliar modelos
    def treinar_e_avaliar_modelo(modelo, x_train, y_train, x_test, y_test, nome_modelo):

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
        st.write(f"Relatórios de Classificação TESTE:")
        acuracia = accuracy_score(y_test, y_pred)
        st.write(f"Acurácia: {acuracia:.2f}")
        st.dataframe(pd.DataFrame(relatorio_renomeado_teste).transpose())
        st.write(f"Relatórios de Classificação TREINO:")
        acuracia_treino = accuracy_score(y_train, y_train_pred)
        st.write(f"Acurácia: {acuracia_treino:.2f}")
        st.dataframe(pd.DataFrame(relatorio_renomeado_treino).transpose())

    # Executar e avaliar o modelo selecionado

    if modelo_selecionado:
        treinar_e_avaliar_modelo(modelos[modelo_selecionado], x_train, y_train, x_test, y_test, modelo_selecionado)