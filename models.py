from pydantic import BaseModel

class ChatModel(BaseModel):
    message: str

class ChatResponseModel(BaseModel):
    response: str