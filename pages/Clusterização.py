import streamlit as st
import nbformat
import requests

# Função para carregar o notebook diretamente do GitHub
def load_notebook_from_github(repo_url, notebook_name):
    # A URL para obter a versão bruta do notebook no GitHub
    notebook_url = f"{repo_url}/raw/main/{notebook_name}"
    
    try:
        response = requests.get(notebook_url)
        response.raise_for_status()  # Levanta um erro em caso de falha
        notebook_content = nbformat.read(response.text, as_version=4)
        return notebook_content
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao carregar o notebook: {e}")
        return None

# Função para exibir células de código e markdown no Streamlit
def display_notebook(notebook_content):
    if notebook_content is None:
        st.error("Não foi possível carregar o notebook.")
        return
    for cell in notebook_content.cells:
        if cell.cell_type == 'code':
            st.subheader("Código")
            st.code(''.join(cell.source.splitlines()), language='python')
            if cell.outputs:
                for output in cell.outputs:
                    if 'text/plain' in output.data:
                        st.write(output.data['text/plain'])
                    elif 'image/png' in output.data:
                        st.image(output.data['image/png'])
                    elif 'text/html' in output.data:
                        st.markdown(output.data['text/html'], unsafe_allow_html=True)
        elif cell.cell_type == 'markdown':
            st.subheader("Comentário")
            st.markdown(cell.source)

# URL do repositório GitHub
repo_url = 'https://github.com/heldjow/PISI3_grupo04_2024.2/raw/main/notebook/Clusterização_Maltez.ipynb' # Substitua pelo seu repositório GitHub
notebook_name = 'Clusterização_Maltez.ipynb'  # Substitua pelo nome do seu notebook no repositório

# Carregar e exibir o notebook
notebook_content = load_notebook_from_github(repo_url, notebook_name)
display_notebook(notebook_content)
