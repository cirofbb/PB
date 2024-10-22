from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import uvicorn


app = FastAPI()


# Carregar o arquivo CSV
csv_file = "lixo.csv"
df = pd.read_csv(csv_file)


@app.get("/")
async def root():
   return {"message": "Bem-vindo à API de dados de coleta seletiva"}


@app.get("/dados")
async def get_dados():
   return df.to_dict(orient="records")


class NovoDado(BaseModel):
   Ano: int
   Lixo_recolhido_por_coleta_seletiva: float
   Lixo_Recuperado_Total: float
   Papel_e_papelao: float
   Plasticos: float
   Metais: float
   Vidro: float
   Outros: Optional[float] = None


   class Config:
       schema_extra = {
           "example": {
               "Ano": 2023,
               "Lixo_recolhido_por_coleta_seletiva": 1000.5,
               "Lixo_Recuperado_Total": 800.0,
               "Papel_e_papelao": 300.0,
               "Plasticos": 200.0,
               "Metais": 150.0,
               "Vidro": 100.0,
               "Outros": 50.0
           }
       }


@app.post("/adicionar")
async def adicionar_dado(novo_dado: NovoDado):
   global df
   # Converter o modelo Pydantic para um dicionário
   novo_dado_dict = novo_dado.dict()
  
   # Renomear as chaves para corresponder exatamente às colunas do CSV
   novo_dado_dict["Lixo recolhido por coleta seletiva (t) (CS026)"] = novo_dado_dict.pop("Lixo_recolhido_por_coleta_seletiva")
   novo_dado_dict["Lixo Recuperado Total (t)"] = novo_dado_dict.pop("Lixo_Recuperado_Total")
   novo_dado_dict["Papel e papelão (CS010)"] = novo_dado_dict.pop("Papel_e_papelao")
   novo_dado_dict["Plásticos (CS011)"] = novo_dado_dict.pop("Plasticos")
   novo_dado_dict["Metais (CS012)"] = novo_dado_dict.pop("Metais")
   novo_dado_dict["Vidro (CS013)"] = novo_dado_dict.pop("Vidro")
   novo_dado_dict["Outros (CS014)"] = novo_dado_dict.pop("Outros")


   # Adicionar o novo dado ao DataFrame
   df = df.append(novo_dado_dict, ignore_index=True)
  
   # Salvar o DataFrame atualizado de volta ao arquivo CSV
   df.to_csv(csv_file, index=False)
  
   return {"mensagem": f"Novo dado adicionado com sucesso para o ano {novo_dado.Ano}"}


if __name__ == "__main__":
   uvicorn.run(
       "TP3:app", 
       host="127.0.0.1",
       port=8010,
       reload=True
   )
