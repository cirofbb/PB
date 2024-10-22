import requests

url = "http://localhost:8010/adicionar"
data = {
    "Ano": 2023,
    "Lixo_recolhido_por_coleta_seletiva": 1000.5,
    "Lixo_Recuperado_Total": 800.0,
    "Papel_e_papelao": 300.0,
    "Plasticos": 200.0,
    "Metais": 150.0,
    "Vidro": 100.0,
    "Outros": 50.0
}

response = requests.post(url, json=data)
print(response.json())