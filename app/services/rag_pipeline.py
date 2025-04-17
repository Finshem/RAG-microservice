from app.services.file_parser import parse_file
from app.services.embedder import get_embeddings
from app.services.vector_store import search_similar_chunks

async def rag_process(file, query: str, chunk_size: int = 500):
    full_text = parse_file(file)
    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    chunk_embeddings = await get_embeddings(chunks)
    query_embedding = (await get_embeddings([query]))[0]
    corpus = list(zip(chunks, chunk_embeddings))
    return search_similar_chunks(query_embedding, corpus)
