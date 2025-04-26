from app.services.file_parser import parse_file
from app.services.embedder import embed_texts
from app.services.vector_store import search_similar_chunks

async def rag_process(file, query: str, chunk_size: int = 500):
    # 1. Extract raw text
    full_text = parse_file(file)

    # 2. Split into chunks
    chunks = [
        full_text[i : i + chunk_size]
        for i in range(0, len(full_text), chunk_size)
    ]

    # 3. Embed your chunks & query (embed_texts is synchronous)
    chunk_embeddings = embed_texts(chunks)
    query_embedding  = embed_texts([query])[0]

    # 4. Pair up and run similarity search
    corpus = list(zip(chunks, chunk_embeddings))
    return search_similar_chunks(query_embedding, corpus)