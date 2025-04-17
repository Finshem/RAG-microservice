from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    prompt: str

class ChatResponse(BaseModel):
    response: str
