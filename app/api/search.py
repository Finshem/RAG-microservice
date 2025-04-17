from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.schemas.search_schema import SearchResponse
from app.services.rag_pipeline import rag_process
from loguru import logger

router = APIRouter()

@router.post("/search_data", response_model=SearchResponse)
async def search_data(file: UploadFile = File(...), query: str = Form(...)):
    try:
        logger.info(f"Received search request: file={file.filename}, query={query}")
        results = await rag_process(file, query)
        return {"results": results}
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
