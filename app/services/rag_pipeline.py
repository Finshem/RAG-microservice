from app.services.file_parser import parse_file
from app.services.embedder import embed_texts, embed_query
from app.services.vector_store import search_similar_chunks
from fastapi import HTTPException

async def rag_process(
    file,                   # UploadFile
    query: str,
    chunk_size: int = 500
):
    # 0) Read file bytes
    contents = await file.read()

    # 1) Parse file into type and text chunks
    filetype, chunks = parse_file(file.filename, contents)
    if filetype != "text":
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type for chat: {file.filename}"
        )

    # 2) Embed chunks and query
    chunk_embeddings = embed_texts(chunks)
    # embed_query returns a single vector
    query_embedding = embed_query(query)

    # 3) Run similarity search
    corpus = list(zip(chunks, chunk_embeddings))
    return search_similar_chunks(query_embedding, corpus)