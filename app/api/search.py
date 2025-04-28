from app.utils.file_types import ALL_MIMES
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from loguru import logger

from app.services.file_parser import parse_file
from app.services.embedder import embed_texts, embed_query
from app.services.text_faiss_index import TextVectorIndex
from app.services.tabular_index import TabularIndex

router = APIRouter()

@router.post("/search_data/")
async def search_data(
    files: List[UploadFile] = File(...),
    query: str = Form(...)
):
    # 0) fresh, empty indexes for each request
    text_index = TextVectorIndex()
    tabular_index = TabularIndex()

    try:
        all_text_chunks = []
        all_text_sources = []

        # 1) Read & parse each file
        for file in files:
            # Validate MIME type
            if file.content_type not in ALL_MIMES:
                raise HTTPException(
                    status_code=400,
                    detail=f"{file.filename}: unsupported media type {file.content_type}"
                )
            # Read contents
            contents = await file.read()
            # Validate file size
            if len(contents) > 100 * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail=f"{file.filename} exceeds 100MB limit."
                )

            filetype, chunks = parse_file(file.filename, contents)

            if filetype == "text":
                all_text_chunks.extend(chunks)
                all_text_sources.extend([file.filename] * len(chunks))
            elif filetype == "table":
                tabular_index.add_table(file.filename, chunks)

        # 2) Dense (FAISS) text search
        text_results = []
        if all_text_chunks:
            embeddings = embed_texts(all_text_chunks)
            text_index.add_documents(
                embeddings=embeddings,
                chunks=all_text_chunks,
                sources=all_text_sources
            )
            query_vec = embed_query(query)
            text_results = text_index.search(query_vec)

        # 3) Sparse (tabular) search
        table_results = tabular_index.search(query)

        # 4) Merge & sort by the original 'score'
        combined = text_results + table_results
        combined.sort(key=lambda x: x.get("score", 0), reverse=True)

        # 5) Remap to unified schema with separate scores
        unified = []
        for item in combined:
            s = float(item.get("score", 0))
            if item.get("type") == "text":
                unified.append({
                    "chunk": item.get("chunk"),
                    "type": "text",
                    "source": item.get("source"),
                    "cosine_distance": s,
                    "semantic_metric": 0.0,
                })
            else:
                unified.append({
                    "chunk": item.get("chunk"),
                    "type": "table",
                    "source": item.get("source"),
                    "cosine_distance": 0.0,
                    "semantic_metric": s,
                })

        return JSONResponse(content=unified)

    except Exception:
        logger.exception("Error in /search_data/")
        raise HTTPException(status_code=500, detail="Internal server error")