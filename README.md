# RAG Microservice

Микросервис для семантического поиска и генерации текста (Retrieval‑Augmented Generation, **RAG**).

## 🚀 Быстрый старт

```bash
git clone https://github.com/Finshem/RAG-microservice.git
cd rag_microservice

cp .env.example .env       
docker compose up --build  
```

После запуска Swagger UI будет доступен по адресу <http://localhost:8000/docs>.

## 📖 Документация API

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/api/search_data` | Поиск релевантных фрагментов в документе. |
| `POST` | `/api/chat_llm` | Генерация ответа на основе найденных фрагментов. |

<details>
<summary>Примеры запросов</summary>

### `/api/search_data`

**Request**

- Файл: `example.pdf`
- Текст запроса: `Какие технологии используются в RAG?`

**Response**

```json
[
  {
    "chunk": "В RAG используются технологии NLP и векторного поиска.",
    "cosine_distance": 0.123,
    "semantic_metric": 0.876
  }
]
```

### `/api/chat_llm`

**Request**

- Файл: `example.txt`
- Текст запроса: `Объясни принцип работы RAG.`
- Промпт: `Ответь как эксперт в области машинного обучения.`

**Response**

```json
{
  "response": "RAG — это методология, которая объединяет поиск информации из внешних источников с генерацией текста с помощью языковых моделей. Это позволяет модели использовать актуальные данные для создания точных и информативных ответов."
}
```

</details>

## ⚙️ Переменные окружения

| Переменная          | Назначение      | Пример   |
|---------------------|-----------------|----------|
| `OPENAI_API_KEY`    | Ключ OpenAI     | `sk-…`   |

## 🧪 Тестовый режим

По умолчанию сервис работает в offline‑режиме: вместо OpenAI вызываются моки (см. `services/embedder.py`, `api/chat.py`).
Чтобы включить реальный LLM, задайте `OPENAI_API_KEY` в `.env`.

## 🛠️ Разработка

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

