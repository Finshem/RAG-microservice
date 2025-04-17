from pydantic import BaseModel
from typing import List

class SearchResult(BaseModel):
    chunk: str
    cosine_distance: float
    semantic_metric: float

class SearchResponse(BaseModel):
    results: List[SearchResult]
