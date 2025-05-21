import requests
import streamlit as st

def fetch_apidata(api_url, headers, method='GET'):
    try:
        if method == 'POST':
            response = requests.post(api_url, headers=headers)
        else:
            response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Lança um erro para códigos de resposta 4xx/5xx
        return response.json()  # Converte o JSON da API em um objeto Python
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao conectar à API: {e}")
        return response.json()