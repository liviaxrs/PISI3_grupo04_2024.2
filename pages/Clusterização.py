import streamlit as st
import pandas as pd
import plotly.express as px # type: ignore

# Título da página
st.markdown("<h1 style='text-align: center;'>Desvendando Perfis de Estudantes</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Insights Através de Clusters 💡</h3>", unsafe_allow_html=True)

# Carregar o dataset
df = pd.read_parquet('pisi3_database/predict_dropout_pt.parquet')

# Criar abas
tab1, tab2, tab3 = st.tabs(["Escolha dos Clusters", "Insights", "Perfis"])

# Aba 1: Escolha dos Clusters
with tab1:
    st.header("Escolha dos Clusters 🫂")
    st.write("Análise para determinar o número ideal de clusters para o conjunto de dados")

    # Método do Cotovelo
    st.subheader("Método do Cotovelo")
    st.image("images/metodoCotovelo.png", caption="Método do Cotovelo para escolha do número de clusters.")
    st.write("""
    O **método do cotovelo** ajuda a identificar o número de clusters que melhor representam os dados.
    O ponto onde a curva forma um "cotovelo" indica o número ideal de clusters.
    """)

    # Coeficiente da Silhueta
    st.subheader("Gráfico da Silhueta")
    st.image("images/coefSilhueta.png", caption="Coeficiente da Silhueta para avaliação da qualidade dos clusters.")
    st.write("""
    O **Coeficiente da Silhueta** é uma métrica usada para avaliar a qualidade dos clusters. Ele mede quão bem cada ponto de dados se encaixa em seu cluster.
    O número ideal de clusters é aquele que maximiza o coeficiente médio da silhueta.
    Para este conjunto de dados foram feitos testes com 2,3 e 4 clusters. 
    A configuração com 3 clusters apresentou uma maior média de silhueta e pontos melhor distribuidos.
    """)
    

# Aba 2: Insights
with tab2:
    st.header("Insights dos Clusters")

    # Heatmaps
    st.subheader("Mapas de Calor")
    colunas_heatmap = ["Qualificação da mãe", "Qualificação do pai"]
    for column in colunas_heatmap:
        df_counts = df.groupby(["Cluster", column]).size().reset_index(name="Quantidade")
        fig = px.density_heatmap(
            df_counts,
            x="Cluster",
            y=column,
            z="Quantidade",
            text_auto=True,
            title=f"Mapa de Calor da {column} por Cluster",
            labels={"Quantidade": "Número de Amostras", "Cluster": "Cluster"},
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig)
    st.write("""
            **Insight para qualificação dos pais:**
            - O **Cluster 0** possui maior distribuição de pais com maior grau de ensino.
            - No **Cluster 1** alunos com pais que tiveream menor grau de ensino possuem tendencia de pertencer a este cluster.
            - O **Cluster 2**, tem maior distribuição de pais que completaram ensino médio ou fundamental.
             """)

    # Gráficos de barras para colunas binárias
    st.subheader("Distribuição de Variáveis Binárias por Cluster")
    colunas_binarias = ['Devedor', 'Bolsista', 'Mensalidade em dia']
    for column in colunas_binarias:
        df_counts = df.groupby(["Cluster", column]).size().reset_index(name="Contagem")
        fig = px.bar(
            df_counts,
            x=column,
            y='Contagem',
            color="Cluster",
            barmode="group",
            title=f"Distribuição de {column} por Cluster"
        )
        st.plotly_chart(fig)
    st.write("""
            **Insight para condições econômicas:**
            - O **Cluster 0** possui uma maior quantidade de não devedores, com as mensalidades em dia e não bolsista.
            - O **Cluster 1** tem uma menor quantidade de não devedores e também com menos mensalidades em dia.
            - No **Cluster 2**, tem um meio termo na quantidade de devedores, mensalidades em dia e com maior quantidade de bolsistas.  
            """)

    # Gráficos de barras para colunas categóricas
    st.subheader("Distribuição de Variáveis Categóricas por Cluster")

   
    colunas_categoricas = ['Estado civil', 'Faixa etária']
    for column in colunas_categoricas:
        df_counts = df.groupby(["Cluster", column]).size().reset_index(name="Contagem")
        fig = px.bar(
            df_counts,
            x='Contagem',
            y=column,
            color="Cluster",
            barmode="group",
            title=f"Distribuição de {column} por Cluster"
        )
        st.plotly_chart(fig)
    st.write("""
    **Insight para Faixa Etária e Estado Cívil:**
    - O **Cluster 0** é predominantemente composto por estudantes jovens entre 18-27 anos e solteiros.
    - O **Cluster 1** tem uma distribuição maior a partir dos 28 anos em relação aos outros clusters, também possui alta distribuição entre os casados e solteiros.
    - No **Cluster 2** também tem proporção maior de estudantes na faixa de 18-27 anos e solteiros.
    - Divorciados e viúvos não tem tanto impacto na formação dos clusters.
    """)


with tab3:
    st.header("Explore os Clusters")

    # Filtros interativos
    st.subheader("Filtros")
    faixa_etaria = st.selectbox("Faixa etária", ["Todas", "18-27 anos", "28-37 anos", "38-47 anos", "48-57 anos", "58-62 anos"])
    estado_civil = st.selectbox("Estado civil", ["Todos", "Solteiro", "Casado", "Divorciado", "Viúvo"])
    qualificacao_mae = st.selectbox("Qualificação da mãe", ["Todas", "Ensino Secundário - 12.º Ano", "Ensino Superior - Bacharelado", "Ensino Básico 3º Ciclo", "Desconhecido", "Ensino básico 1º ciclo", "Ensino Básico 2.º Ciclo", "Outro", "Ensino superior - Licenciatura", "Ensino superior - Mestrado"])
    qualificacao_pai = st.selectbox("Qualificação do pai", ["Todas", "Ensino Secundário - 12.º Ano", "Ensino Superior - Bacharelado", "Ensino Básico 3º Ciclo", "Desconhecido", "Ensino básico 1º ciclo", "Ensino Básico 2.º Ciclo", "Outro", "Ensino superior - Licenciatura", "Ensino superior - Mestrado"])
    devedor = st.selectbox("É devedor?", ["Todos", "Sim", "Não"])
    bolsista = st.selectbox("É bolsista?", ["Todos", "Sim", "Não"])

    # Aplicar filtros
    filtered_df = df.copy()
    if faixa_etaria != "Todas":
        filtered_df = filtered_df[filtered_df["Faixa etária"] == faixa_etaria]
    if estado_civil != "Todos":
        filtered_df = filtered_df[filtered_df["Estado civil"] == estado_civil]
    if qualificacao_mae != "Todas":
        filtered_df = filtered_df[filtered_df["Qualificação da mãe"] == qualificacao_mae]
    if qualificacao_pai != "Todas":
        filtered_df = filtered_df[filtered_df["Qualificação do pai"] == qualificacao_pai]
    if devedor != "Todos":
        filtered_df = filtered_df[filtered_df["Devedor"] == devedor]
    if bolsista != "Todos":
        filtered_df = filtered_df[filtered_df["Bolsista"] == bolsista]

    # Exibir distribuição dos clusters
    st.subheader("Distribuição dos Clusters")

    if not filtered_df.empty:
        cluster_counts = filtered_df["Cluster"].value_counts().reset_index()
        cluster_counts.columns = ["Cluster", "Quantidade"]

        # Gráfico de barras
        fig = px.bar(
            cluster_counts,
            x="Cluster",
            y="Quantidade",
            title="Distribuição dos Clusters",
            labels={"Quantidade": "Número de Estudantes", "Cluster": "Cluster"},
            color="Cluster",
            text_auto=True
        )
        st.plotly_chart(fig)

        # Descrição dos clusters
        st.subheader("Descrição dos Clusters")
        cluster_descriptions = {
            0: """🧑‍🎓 Jovens abastados 

        - Caracteristicas:
        - Pais com maior grau de ensino  
        - Não devedor  
        - Mensalidades em dia  
        - Não bolsista  
        - Jovens entre 18-27 anos  
        - Solteiros  
        """,
            1: """🧑‍🏫 Experientes com pouco dinheiro
        
        - Caracteristicas:
        - Pais com menor grau de ensino  
        - Menor quantidade de não devedores  
        - Menos mensalidades em dia  
        - A partir dos 28 anos  
        - Casados ou solteiros  
        """,
            2: """🎓 Bolsistas meio termo 

        - Caracteristicas:
        - Pais que completaram ensino médio ou fundamental  
        - Bolsistas  
        - Jovens entre 18-27 anos  
        - Solteiros  
        """
        }
        for cluster, desc in cluster_descriptions.items():
            st.write(f"**Cluster {cluster}:** {desc}")
    else:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")