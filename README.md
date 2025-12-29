# RST Discourse Parser API

REST API обертка над `isanlp_rst` для дискурсивного анализа (RST) английских текстов. Использует модель `gumrrg`.

## Быстрый старт

Требуется [uv](https://github.com/astral-sh/uv).

```bash
# 1. Установка
git clone <repo>
cd PythonDisourseParser
uv sync

# 2. Запуск
uv run python main.py
```

Сервер доступен по адресу: `http://127.0.0.1:8000`

## API

### `POST /parse`

Анализ текста и построение дерева дискурса.

**Запрос:**
```json
{ "text": "Although it was raining, we went out." }
```

**Ответ:**
```json
{
  "tree": {
    "id": 1,
    "relation": "Contrast",
    "nuclearity": "NS",
    "children": [
      {
        "id": 2,
        "relation": "elementary",
        "nuclearity": "N",
        "text": "Although it was raining ,",
        "children": []
      },
      {
        "id": 3,
        "relation": "elementary",
        "nuclearity": "S",
        "text": "we went out .",
        "children": []
      }
    ]
  }
}
```

## Тестирование

Скрипт `test_api.py` содержит примеры сложных предложений для проверки парсера.

```bash
uv run python test_api.py
```

## Детали реализации

- **Модель**: `gumrrg` (GUM corpus, Rhetorical Relations Group).
- **Библиотека**: `isanlp_rst` v3.
- **Фреймворк**: FastAPI.
