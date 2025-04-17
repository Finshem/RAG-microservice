from app.services.vector_store import search_similar_chunks

def test_vector_similarity():
    corpus = [("text1", [1.0, 0.0]), ("text2", [0.0, 1.0])]
    query = [0.9, 0.1]
    result = search_similar_chunks(query, corpus, top_k=1)
    assert isinstance(result, list)
    assert "chunk" in result[0]
