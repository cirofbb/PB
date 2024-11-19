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


try:
   response = requests.post(url, json=data)
   print(f"Status Code: {response.status_code}")
   print(f"Response Content: {response.text}")
  
   response.raise_for_status()  
  
   if response.headers.get('content-type') == 'application/json':
       print(f"JSON Response: {response.json()}")
   else:
       print("Response is not in JSON format")
except requests.exceptions.HTTPError as errh:
   print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
   print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
   print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
   print(f"An error occurred: {err}")