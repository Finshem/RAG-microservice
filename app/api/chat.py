from app.utils.file_types import ALL_MIMES
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.schemas.chat_schema import ChatResponse
from app.services.rag_pipeline import rag_process
from loguru import logger

router = APIRouter()

@router.post("/chat_llm", response_model=ChatResponse)
async def chat_llm(
    file: UploadFile = File(...),
    query: str = Form(...),
    prompt: str = Form(...)
):
    try:
        # Log incoming request
        logger.info(f"Received chat request: file={file.filename}, query={query!r}, prompt={prompt!r}")

        # Validate MIME type
        if file.content_type not in ALL_MIMES:
            raise HTTPException(
                status_code=400,
                detail=f"{file.filename}: unsupported media type {file.content_type}"
            )

        # Process file and query through RAG pipeline
        chunks = await rag_process(file, query)
        logger.debug(f"Chunks received for chat: {chunks}")

        # Validate structure of chunks
        if not chunks or not isinstance(chunks, list) or not isinstance(chunks[0], dict) or "chunk" not in chunks[0]:
            logger.warning("Invalid chunks structure")
            raise HTTPException(status_code=500, detail="Invalid chunks structure")

        # Build context from chunks
        context = "\n".join(item["chunk"] for item in chunks)

        # Mocked response (replace with actual OpenAI call later)
        mocked_response = f"<Mocked response on query: '{query}' with prompt: '{prompt}' and {len(chunks)} chunks>"
        return {"response": mocked_response}

    except HTTPException:
        # Propagate HTTP errors
        raise
    except Exception as e:
        logger.exception("Chat error")
        raise HTTPException(status_code=500, detail="Internal server error")