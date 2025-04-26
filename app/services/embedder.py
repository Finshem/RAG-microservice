from sentence_transformers import SentenceTransformer
import numpy as np

_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(chunks):
    return _model.encode(chunks, show_progress_bar=False, convert_to_numpy=True)

def embed_query(query):
    return _model.encode([query], convert_to_numpy=True)[0]
