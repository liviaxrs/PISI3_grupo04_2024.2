## 🚀 Visão Geral
Este projeto foi desenvolvido para a disciplina de Projeto Interdisciplinar para Sistemas de Informação do curso de Bacharelado em Sistemas de Informação.

## 🎯 Objetivo
- O principal objetivo deste estudo é desenvolver um modelo preditivo para auxiliar universidades na identificação precoce de alunos em risco, permitindo a implementação de estratégias preventivas.
- Como parte da documentação do projeto, foi elaborado um **[artigo acadêmico](https://docs.google.com/document/d/1uz-vS85vV6dmAmyaqbaPhqELs5fBSofPZnKJj427PFM/edit?usp=sharing)** detalhando o processo de desenvolvimento dos modelos e a análise dos resultados.
- Além disso, foi criado um **[aplicativo em Streamlit](https://pisi3-grupo04.streamlit.app/)** para a visualização interativa do dataset por meio de gráficos e para que os usuários possam utilizar o modelo já treinado.

## 📊 Conjunto de Dados
Para o treinamento do modelo e análise dos dados, foi utilizado o dataset **[Predict Students Dropout and Academic Success](https://www.kaggle.com/datasets/syedfaizanalii/predict-students-dropout-and-academic-success)**.

## 🖥 Funcionalidades do Streamlit
A aplicação desenvolvida em **Streamlit** permite que os usuários interajam com os dados e os modelos de machine learning de forma intuitiva. As principais funcionalidades incluem:

### 🔍 Análise Exploratória
- Visualização interativa dos dados por meio de **gráficos dinâmicos** (histogramas, boxplots, scatter plots, etc.).
- Estatísticas descritivas das principais variáveis do dataset.

### 🤖 Modelos de Classificação
- Treinamento e comparação de diversos modelos de machine learning.
- Exibição de **métricas de desempenho** como acurácia, precisão, recall e F1-score.

### 🎯 Teste do Modelo
- Área interativa onde o usuário pode **inserir seus próprios dados** para testar a previsão do modelo final escolhido.

### 🔗 Clusterização
- Aplicação do algoritmo **K-Means** para agrupar os alunos com base em características semelhantes.
- Visualização dos clusters em gráficos interativos para melhor compreensão dos padrões encontrados.

## 🔧 Tecnologias Utilizadas
- **Python** (pandas, numpy, scikit-learn, matplotlib, seaborn)
- **Jupyter Notebook**
- **Streamlit** (para visualização dos modelos e previsões)
- **Pickle** (para salvar e carregar modelos treinados)

## 🖥 Como Executar o Projeto
1. Clone este repositório:
   ```bash
   git clone https://github.com/liviaxrs/PISI3_grupo04_2024.2
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o **notebook de treinamento**:
   ```bash
   jupyter notebook
   ```
4. Para rodar a interface em **Streamlit**:
   ```bash
   streamlit run app.py
   ```
4. Para rodar a interface em **Streamlit**:
   ```bash
   streamlit run app.py
   ```
