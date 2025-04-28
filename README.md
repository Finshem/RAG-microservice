# RAG Microservice

## 📌 Описание

Микросервис на FastAPI + Docker, реализующий Retrieval-Augmented Generation (RAG) с поддержкой:

- **Мультизагрузки** документов
- **Гибридного поиска**:
  - **Dense (FAISS)** для текстовых чанков → `cosine_distance`
  - **Sparse (таблицы)** через ключевые поисковые методы → `semantic_metric`
- **Chat-LLM** эндпоинта для генерации ответа на основе найденных чанков (опционально)
- Подробное **логирование** в консоль и в файл `app.log`
- **Валидация** типов и ограничения по размеру файлов (≤100 МБ)

---

## 🚀 Быстрый старт

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Finshem/RAG-microservice.git
cd RAG-microservice

# 2. Создать .env на основе примера и заполнить значения
cp .env.example .env

# 3. Запустить сервис
docker compose up -d

# API доступен на http://localhost:8000
# Swagger UI — http://localhost:8000/docs
```

---

## ⚙️ Переменные окружения (`.env`)

```ini
OPENAI_API_URL=https://api.openai.com/v1/chat/completions
OPENAI_API_KEY=your_token_here
MODEL=gpt-4o
TEMPERATURE=0.7
MAX_TOKENS=512
```

---

## 📂 Поддерживаемые форматы

- **.pdf**
- **.txt**
- **.html**
- **.csv**
- **.xlsx**

> **Максимальный размер каждого файла:** 100 МБ\
> **Ошибка 400**, если формат не из списка или файл > 100 МБ.

---

## 📘 Эндпоинты

### 🔍 `POST /api/search_data/` — гибридный поиск

**Функционал:**

- Загружает файлы любых поддерживаемых типов
- Исключает файлы > 100 МБ и неподдерживаемые MIME-типы (400)
- Делает векторный поиск по тексту (FAISS) → `cosine_distance`
- Делает sparse-поиск по таблицам → `semantic_metric`
- Возвращает объединённый и отсортированный по `score` результат

**Request (multipart/form-data):**

- `files`: UploadFile[]
- `query`: string

**Response 200 OK:**

```json
[
  {
    "chunk": "… текстовый фрагмент …",
    "type": "text",
    "source": "report.pdf",
    "cosine_distance": 0.912,
    "semantic_metric": 0.0
  },
  {
    "chunk": "row1 | row2 | …",
    "type": "table",
    "source": "data.xlsx",
    "cosine_distance": 0.0,
    "semantic_metric": 1.0
  }
]
```

**Errors:**

- 400 Bad Request — неподдерживаемый формат или файл > 100 МБ
- 500 Internal Server Error — непредвиденная ошибка

---

### 💬 `POST /api/chat_llm` — генерация от LLM

**Функционал:**

- Загружает **1 файл** (текстовый)
- Делает те же RAG-процедуры, возвращает top-N чанков
- Формирует контекст + `prompt` и шлёт в OpenAI
- Возвращает ответ модели

**Request (multipart/form-data):**

- `file`: UploadFile
- `query`: string
- `prompt`: string

**Response 200 OK:**

```json
{
  "response": "<ответ LLM на основе найденных чанков>"
}
```

**Errors:**

- 400 Bad Request — неподдерживаемый формат или файл > 100 МБ
- 500 Internal Server Error — непредвиденная ошибка

---

## 🧪 Примеры CURL-запросов

1️⃣ **Однофайловый поиск**

```bash
curl -s -X POST http://localhost:8000/api/search_data/ \
  -F "files=@example.txt" \
  -F "query=Retrieval-Augmented Generation" | jq .
```

2️⃣ **Двухфайловый поиск**

```bash
curl -s -X POST http://localhost:8000/api/search_data/ \
  -F "files=@example.txt" \
  -F "files=@example.csv" \
  -F "query=vector search" | jq .
```

3️⃣ **Пятифайловый поиск**

```bash
curl -s -X POST http://localhost:8000/api/search_data/ \
  -F "files=@example.txt" \
  -F "files=@example.html" \
  -F "files=@example.csv" \
  -F "files=@example.xlsx" \
  -F "files=@example.pdf" \
  -F "query=hybrid search" | jq .
```

4️⃣ **Chat-LLM**

```bash
curl -s -X POST http://localhost:8000/api/chat_llm \
  -F "file=@example.txt" \
  -F "query=Explain RAG" \
  -F "prompt=Answer as an ML expert." | jq .
```

---

## 🪵 Логирование

- **Консоль**: INFO, DEBUG, ERROR
- **Файл**: `app.log` (Loguru, ротация 10 МБ)