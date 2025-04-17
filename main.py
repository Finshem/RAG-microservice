from fastapi import FastAPI
from app.api.search import router as search_router
from app.api.chat import router as chat_router
from app.core.logger import setup_logging
from app.core.config import settings

setup_logging()

app = FastAPI(title="RAG Microservice")

app.include_router(search_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
