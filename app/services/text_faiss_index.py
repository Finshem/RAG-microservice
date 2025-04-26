# app/services/text_faiss_index.py

import faiss
import numpy as np
from typing import List, Dict

class TextVectorIndex:
    def __init__(self):
        self.index = faiss.IndexFlatIP(384)  # 384 = размерность 'all-MiniLM-L6-v2'
        self.vectors = []
        self.chunks = []
        self.sources = []

    def add_documents(self, embeddings: np.ndarray, chunks: List[str], sources: List[str]):
        if not self.index.is_trained:
            raise ValueError("FAISS index is not trained")
        
        self.index.add(embeddings)
        self.vectors.extend(embeddings)
        self.chunks.extend(chunks)
        self.sources.extend(sources)

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Dict]:
        if len(self.chunks) == 0:
            return []

        query_vector = np.expand_dims(query_vector, axis=0)
        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx == -1: continue
            results.append({
                "chunk": self.chunks[idx],
                "score": float(score),
                "type": "text",
                "source": self.sources[idx]
            })

        return results