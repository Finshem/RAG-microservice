from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.schemas.chat_schema import ChatResponse
from app.services.rag_pipeline import rag_process
from loguru import logger

router = APIRouter()

@router.post("/chat_llm", response_model=ChatResponse)
async def chat_llm(file: UploadFile = File(...), query: str = Form(...), prompt: str = Form(...)):
    try:
        logger.info(f"Received chat request: file={file.filename}, query={query}, prompt={prompt}")
        
        chunks = await rag_process(file, query)
        logger.debug(f"Chunks received for chat: {chunks}")  # 👈 Логируем, что вернулось

        # Проверим структуру chunks перед сборкой context
        if not chunks or not isinstance(chunks, list) or "chunk" not in chunks[0]:
            logger.warning("Invalid chunks structure")
            raise ValueError("Invalid chunks structure")

        context = "\n".join(chunk["chunk"] for chunk in chunks)

        # Мок-ответ (пока без вызова OpenAI API)
        mocked_response = f"<Mocked response on query: '{query}' with prompt: '{prompt}' and {len(chunks)} chunks>"
        return {"response": mocked_response}

    except Exception as e:
        logger.exception("Chat error")  # 👈 Логируем полный traceback
        raise HTTPException(status_code=500, detail="Internal server error")

