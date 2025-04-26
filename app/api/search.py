# app/api/search.py (рефакторинг под мультизагрузку и гибридный поиск)

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from loguru import logger

from app.services.file_parser import parse_file
from app.services.embedder import embed_texts, embed_query
from app.services.text_faiss_index import TextVectorIndex
from app.services.tabular_index import TabularIndex

router = APIRouter()

# Инициализация индексов (в памяти)
text_index = TextVectorIndex()
tabular_index = TabularIndex()

@router.post("/search_data/")
async def search_data(files: List[UploadFile] = File(...), query: str = Form(...)):
    try:
        all_text_chunks = []
        all_text_sources = []

        for file in files:
            contents = await file.read()
            if len(contents) > 100 * 1024 * 1024:
                raise HTTPException(status_code=400, detail=f"{file.filename} exceeds 100MB limit.")

            filetype, chunks = parse_file(file.filename, contents)

            if filetype == "text":
                all_text_chunks.extend(chunks)
                all_text_sources.extend([file.filename] * len(chunks))

            elif filetype == "table":
                tabular_index.add_table(file.filename, chunks)

        # Обработка текстового поиска
        text_results = []
        if all_text_chunks:
            doc_embeddings = embed_texts(all_text_chunks)
            text_index.add_documents(doc_embeddings, all_text_chunks, all_text_sources)
            query_vector = embed_query(query)
            text_results = text_index.search(query_vector)

        # Обработка табличного поиска
        table_results = tabular_index.search(query)

        # Объединение
        combined = text_results + table_results
        combined.sort(key=lambda x: x.get("score", 0), reverse=True)

        return JSONResponse(content=combined)

    except Exception as e:
        logger.exception("Error in /search_data/")
        raise HTTPException(status_code=500, detail=str(e))

