from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.search import router as search_router
from app.api.chat import router as chat_router
from app.core.logger import setup_logging
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.config import settings

setup_logging()

app = FastAPI(title="RAG Microservice")

MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB

class LimitUploadSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_UPLOAD_SIZE:
            return JSONResponse(
                status_code=413,
                content={"detail": "File too large. Max size is 100MB."}
            )
        return await call_next(request)

app.add_middleware(LimitUploadSizeMiddleware)

app.include_router(search_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
