import requests
from config import API_URL, USR_API, PWD_API

def getToken():
    # Defina a URL do endpoint
    url = API_URL + '/auth/token'
    # Defina os parâmetros a serem enviados
    data = {
        'username': USR_API,
        'password': PWD_API
    }
    # Enviar a solicitação POST para o endpoint
    response = requests.post(url, data=data)
    # Verificar a resposta
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return response.json()
    
def save_to_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def read_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()