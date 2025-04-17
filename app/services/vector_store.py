from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search_similar_chunks(query_vec: list[float], corpus: list[tuple[str, list[float]]], top_k: int = 5):
    vectors = np.array([vec for _, vec in corpus])
    sims = cosine_similarity([query_vec], vectors)[0]
    results = []
    for idx, score in enumerate(sims):
        chunk_text = corpus[idx][0]
        results.append({
            "chunk": chunk_text,
            "cosine_distance": float(1 - score),
            "semantic_metric": float(score)
        })
    return sorted(results, key=lambda x: x["semantic_metric"], reverse=True)[:top_k]
