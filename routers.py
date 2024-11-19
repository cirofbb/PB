from fastapi import APIRouter, HTTPException
from models import ChatModel, ChatResponseModel
import google.generativeai as genai

router = APIRouter()

@router.post("/chat/", response_model=ChatResponseModel)
async def chat(body: ChatModel) -> ChatResponseModel:
    try:
        api_key = "AIzaSyA70KizSuH3iayJPMQEW6BsbhP42E7BP-w"
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        persona = "Você é um assistente amigável especialista em questões de reciclagem e tratamento de resíduos."
        prompt = f"{persona}\nUsuário: {body.message}\nAssistente:"
        
        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise HTTPException(
                status_code=500, 
                detail="Erro ao gerar a resposta. O modelo retornou uma resposta vazia."
            )
        
        return ChatResponseModel(response=response.text)
    
    except genai.exceptions.InvalidApiKeyError:
        raise HTTPException(
            status_code=401,
            detail="Chave de API inválida. Verifique a configuração da chave de API."
        )
