import streamlit as st
import requests

st.set_page_config(page_title="Consulta CEP", page_icon="logo_busca_cep.webp", layout="wide")

st.logo(image="logo_busca_cep.webp", size="large")

# Título da aplicação
st.title("Consultar Endereço")

# Campo de entrada do CEP
entrada_cep = st.text_input(label="Informe o CEP para consulta", max_chars=8)

# Inicializando o estado para os campos
if "dados" not in st.session_state:
    st.session_state.dados = {
        "CEP": "",
        "Tipo Endereço": "",
        "Nome Endereço": "",
        "Bairro": "",
        "Estado": "",
        "Cidade": "",
        "DDD": ""
    }

# Função para pegar os dados do CEP
def pegar_dados():
    cep = entrada_cep.strip()  # Remove espaços extras
    if len(cep) == 8 and cep.isdigit():  # Verifica se o CEP é válido
        with st.spinner("Consultando..."):  # Mostra o spinner enquanto processa
            response = requests.get(f"https://cep.awesomeapi.com.br/json/{cep}")
            if response.status_code == 200:  # Verifica se a resposta foi bem-sucedida
                cep_detalhes = response.json()
                st.session_state.dados.update({
                    "CEP": cep,
                    "Tipo Endereço": cep_detalhes.get("address_type", ""),
                    "Nome Endereço": cep_detalhes.get("address_name", ""),
                    "Bairro": cep_detalhes.get("district", ""),
                    "Estado": cep_detalhes.get("state", ""),
                    "Cidade": cep_detalhes.get("city", ""),
                    "DDD": cep_detalhes.get("ddd", "")
                })
            else:
                st.error(f"Erro ao consultar o CEP: {response.status_code}")
    else:
        st.error("CEP inválido. Digite um CEP com 8 dígitos.")

# Função para limpar os dados
def limpar_dados():
    st.session_state.dados = {
        "CEP": "",
        "Tipo Endereço": "",
        "Nome Endereço": "",
        "Bairro": "",
        "Estado": "",
        "Cidade": "",
        "DDD": ""
    }

# Botões para consultar e limpar
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.button("Consultar", on_click=pegar_dados)
with col2:
    st.button("Limpar", on_click=limpar_dados)

# Exibindo os campos com os valores atualizados
col1, col2, col3, col4 = st.columns(4)
col1.text_input(label="CEP", value=st.session_state.dados["CEP"], disabled=True)
col2.text_input(label="DDD", value=st.session_state.dados["DDD"], disabled=True)
col3.text_input(label="Estado", value=st.session_state.dados["Estado"], disabled=True)
col4.text_input(label="Cidade", value=st.session_state.dados["Cidade"], disabled=True)

col1, col2, col3 = st.columns(3)
col1.text_input(label="Tipo Endereço", value=st.session_state.dados["Tipo Endereço"], disabled=True)
col2.text_input(label="Nome Endereço", value=st.session_state.dados["Nome Endereço"], disabled=True)
col3.text_input(label="Bairro", value=st.session_state.dados["Bairro"], disabled=True)