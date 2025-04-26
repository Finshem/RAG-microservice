# README.md — обновленный с примерами гибридного поиска

# RAG Microservice

## 📌 Описание
Микросервис на FastAPI, реализующий Retrieval-Augmented Generation (RAG) с поддержкой мультизагрузки документов, гибридного поиска (текст + таблицы) и генерации ответа от LLM (опционально).

---

## 🚀 Запуск
```bash
# 1. Клонируй репозиторий
https://github.com/Finshem/RAG-microservice.git

# 2. Перейди в директорию
cd RAG-microservice

# 3. Запусти сервис
docker compose up -d
```

---

## ⚙️ Переменные окружения (.env)
```env
OPENAI_API_URL=https://api.openai.com/v1/chat/completions
OPENAI_API_KEY=your_token_here
MODEL=gpt-4o
TEMPERATURE=0.7
MAX_TOKENS=512
```

---

## 📂 Поддерживаемые форматы
- .pdf
- .txt
- .html
- .csv
- .xlsx

**Максимальный размер каждого файла: 100MB**

---

## 📘 Эндпоинты

### 🔍 `/api/search_data/` — гибридный поиск
**Описание:**
- Принимает **один или несколько** файлов
- Делает **векторный поиск по тексту (FAISS)**
- Делает **ключевой поиск по таблицам**

**Request:**
```http
POST /api/search_data/
Content-Type: multipart/form-data

- files: [UploadFile, UploadFile, ...]
- query: строка запроса
```

**Response:**
```json
[
  {
    "chunk": "...",
    "score": 0.912,
    "type": "text",
    "source": "report.pdf"
  },
  {
    "chunk": "row1 | row2 | ...",
    "score": 1.0,
    "type": "table",
    "source": "data.xlsx"
  }
]
```

---

### 💬 `/api/chat_llm/` — генерация от LLM (опционально)
**Описание:** добавляет top-N чанков к промпту и отправляет в OpenAI.

---

## 🧪 Пример CURL-запроса
```bash
curl -X POST http://localhost:8000/api/search_data/ \
  -F "files=@example.pdf" \
  -F "files=@report.xlsx" \
  -F "query=Какой прогноз по продажам в 2025 году?"
```

---

## 🪵 Логирование
- stdout: INFO, DEBUG, ERROR
- файл: `app.log`

---

## ✅ Требования ТЗ покрыты:
- [x] Гибридный поиск: текст + таблицы
- [x] FAISS векторная база
- [x] Мультидокументная загрузка
- [x] Ограничение по размеру
- [x] Эндпоинты `/search_data/`, `/chat_llm/`
- [x] Докер, .env, README

---

## 🧠 В планах
- Рерангинг результатов
- Интеграция LLM без OpenAI (опционально)