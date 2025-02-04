import streamlit as st
import requests
from nbconvert import HTMLExporter
import nbformat

st.set_page_config(layout="wide")  # Modo de tela larga

# URL do notebook no GitHub
url = "https://raw.githubusercontent.com/LucasGCRamos/PISI3_grupo04_2024.2/refs/heads/main/notebook/Clusteriza%C3%A7%C3%A3o_Lucas.ipynb"

# Função para carregar o notebook e converter para HTML
def load_notebook_as_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        notebook_content = nbformat.reads(response.text, as_version=4)
        html_exporter = HTMLExporter()
        html_data, _ = html_exporter.from_notebook_node(notebook_content)
        return html_data
    else:
        return None

# Streamlit App
st.title("Visualização do Notebook")
st.write("Clusterização_Maltez.ipynb")

# Carregar notebook
html_notebook = load_notebook_as_html(url)

if html_notebook:
    st.components.v1.html(html_notebook, height=1200, scrolling=True)  # Aumenta altura
else:
    st.error("Erro ao carregar o notebook. Verifique o link.")
