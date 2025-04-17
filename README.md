# RAG Microservice

Микросервис для семантического поиска и генерации текста на основе документов (RAG-подход).

## 🚀 Запуск

```bash
cp .env.example .env
docker compose up --build
```

## 📂 Эндпоинты

### `/api/search_data/`

**POST**  
**Поля:**
- `file`: документ
- `query`: текстовый запрос

**Пример ответа:**
```json
{
  "results": [
    {
      "chunk": "...",
      "cosine_distance": 0.12,
      "semantic_metric": 0.88
    }
  ]
}
```

---

### `/api/chat_llm/`

**POST**  
**Поля:**
- `file`: документ
- `query`: вопрос
- `prompt`: системный промпт

**Пример ответа:**
```json
{
  "response": "Ответ модели..."
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
   git clone https://github.com/your-username/rag_microservice.git
   cd rag_microservice
   ```

2. Создать виртуальное окружение и активировать его:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустить сервер:
   ```bash
   uvicorn main:app --reload
   ```

5. Swagger UI будет доступен по адресу:
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