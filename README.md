# RAG Microservice

Микросервис для семантического поиска и генерации текста на основе документов (RAG-подход).

## 🚀 Запуск

```bash
cp .env.example .env
docker compose up --build
```

## 📂 Эндпоинты

### `/api/search_data/`

**Request:**

Файл: `example.pdf`  
Текст запроса: `"Какие технологии используются в RAG?"`

**Response:**
```json
[
  {
    "chunk": "В RAG используются технологии NLP и векторного поиска.",
    "cosine_distance": 0.123,
    "semantic_metric": 0.876
  },
  {
    "chunk": "Методология RAG объединяет поиск по базе данных и генерацию текста.",
    "cosine_distance": 0.456,
    "semantic_metric": 0.765
  }
]
```

---

### `/api/chat_llm/`

**Request:**

Файл: `example.txt`  
Текст запроса: `"Объясни принцип работы RAG."`  
Промпт: `"Ответь как эксперт в области машинного обучения."`

**Response:**
```json
{
  "response": "RAG — это методология, которая объединяет поиск информации из внешних источников с генерацией текста с помощью языковых моделей. Это позволяет модели использовать актуальные данные для создания точных и информативных ответов."
}

```

## 📓 Swagger UI

После запуска:
```
http://localhost:8000/docs
```

## 🚀 Как запустить проект

1. Клонировать репозиторий:
   ```bash
   git clone https://github.com/Finshem/RAG-microservice.git
   cd rag_microservice
   ```

2. Скопировать переменные окружения:
   ```bash
   cp .env.example .env
   ```

3. Собрать и запустить контейнер:
   ```bash
   docker compose up --build
   ```

4. Swagger UI будет доступен по адресу:
   ```
   http://127.0.0.1:8000/docs
   ```

---

## 📡 Вызов endpoints

- `/api/search_data` — принимает файл и запрос (query), возвращает список похожих текстовых фрагментов.
- `/api/chat_llm` — принимает файл, запрос и промпт, возвращает ответ в формате чата.

Оба endpoint'а доступны через Swagger-интерфейс: `http://127.0.0.1:8000/docs`

---

## 🧪 Тестовый режим и моки

- В текущей версии вместо OpenAI используется **мок-ответ** — модель не вызывается, а возвращается заглушка.
- Это сделано для локального тестирования без необходимости наличия API-ключа.
- Поведение реализовано в `services/embedder.py` и `api/chat.py`.

---

## 🛠 Дополнительно (если используете прокси)

Если у вас были установлены переменные окружения прокси, и вы получаете ошибки вида "Unknown scheme for proxy URL", выполните:

```bash
unset http_proxy
unset https_proxy
unset ftp_proxy
unset HTTP_PROXY
unset HTTPS_PROXY
unset FTP_PROXY
unset all_proxy
unset ALL_PROXY
```
