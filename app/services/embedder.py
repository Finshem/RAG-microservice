# services/embedder.py
# import httpx  ← можно оставить или удалить, не важно
# from app.core.config import settings ← тоже не нужен если мок

from typing import List

async def get_embeddings(texts: List[str]) -> List[List[float]]:
    # Мок вместо реального вызова OpenAI API
    return [[0.1, 0.2, 0.3] for _ in texts]

    # Ниже закомментирован оригинальный код
    # headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
    # json_data = {
    #     "input": texts,
    #     "model": settings.model
    # }
    # async with httpx.AsyncClient(proxies=None) as client:
    #     response = await client.post(
    #         url=settings.openai_api_url.replace("/chat/completions", "/embeddings"),
    #         json=json_data,
    #         headers=headers
    #     )
    #     response.raise_for_status()
    #     return [e["embedding"] for e in response.json()["data"]]

