# API Дискурсивного Парсера RST

Этот проект предоставляет REST API для дискурсивного анализа на основе Теории Риторических Структур (RST). Он использует библиотеку `isanlp_rst` и модель `gumrrg` для анализа структуры дискурса текстов на английском языке.

## Возможности

- **RST Парсинг**: Анализирует текст для выявления дискурсивных отношений (например, Уточнение, Контраст, Причина).
- **FastAPI**: Высокопроизводительный и простой в использовании веб-фреймворк.
- **JSON Вывод**: Возвращает дерево разбора в структурированном формате JSON.

## Требования

- Python 3.13+
- Зависимости:
    - `fastapi`
    - `uvicorn`
    - `pydantic`
    - `torch`
    - `transformers`
    - `isanlp`
    - `isanlp-rst`

## Установка

1.  **Клонирование репозитория:**
    ```bash
    git clone <repository-url>
    cd PythonDisourseParser
    ```

2.  **Установка зависимостей:**
    Рекомендуется использовать виртуальное окружение.
    ```bash
    pip install -r requirements.txt
    # ИЛИ, если используется uv/poetry и pyproject.toml
    pip install .
    ```
    
    *Примечание: Возможно, потребуется установить `isanlp` напрямую с GitHub, если он недоступен в PyPI:*
    ```bash
    pip install git+https://github.com/iinemo/isanlp.git
    pip install isanlp-rst
    ```

## Запуск сервера

Вы можете запустить сервер, используя предоставленный скрипт `main.py`:

```bash
python main.py
```

Или используя `uvicorn` напрямую:

```bash
uvicorn main:app --host 127.0.0.1 --port 8052 --reload
```

Сервер запустится по адресу `http://127.0.0.1:8052`.

## Использование API

### Анализ текста

**Эндпоинт:** `POST /parse`

**Тело запроса:**
```json
{
  "text": "Although it was raining heavily, we decided to go for a walk."
}
```

**Ответ:**
Возвращает JSON-объект, представляющий структуру дерева RST.

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
        "text": "Although it was raining heavily ,",
        ...
      },
      {
        "id": 3,
        "relation": "elementary",
        "nuclearity": "S",
        "text": "we decided to go for a walk .",
        ...
      }
    ]
  }
}
```

## Тестирование

Включен тестовый скрипт `test_api.py` для проверки функциональности API на сложных предложениях.

1.  Убедитесь, что сервер запущен.
2.  Запустите тестовый скрипт:

```bash
python test_api.py
```

Этот скрипт отправляет несколько тестовых примеров в API и выводит полученные деревья дискурса.
