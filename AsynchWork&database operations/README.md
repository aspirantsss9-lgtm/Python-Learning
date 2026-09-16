# ДЗ 04 — Асинхронная работа с сетью и БД

## Описание проекта

Проект демонстрирует асинхронную работу с внешним HTTP API и базой данных PostgreSQL с использованием Python, `aiohttp` и SQLAlchemy.

В качестве источника данных используется JSONPlaceholder. Приложение асинхронно получает список пользователей и список публикаций, после чего сохраняет полученные данные в PostgreSQL.

Основная задача проекта — продемонстрировать применение:

* асинхронных HTTP-запросов;
* `asyncio`;
* `asyncio.gather`;
* `aiohttp`;
* асинхронного SQLAlchemy;
* `AsyncSession`;
* ORM-моделей;
* пакетной записи данных в базу данных;
* автоматического запуска тестов через GitHub Actions.

---

## Используемые технологии

* Python 3.13
* aiohttp
* SQLAlchemy
* asyncpg
* PostgreSQL
* pytest
* GitHub Actions

---

## Структура проекта

```text
AsynchWork&database operations/
├── .github/
│   └── workflows/
│       └── run_tests.yml
├── data/
│   └── cache/
├── testing/
│   └── test_homework.py
├── __init__.py
├── jsonplaceholder_requests.py
├── main.py
├── models.py
├── pytest.ini
├── README.md
├── requirements-dev.txt
├── requirements.txt
└── .gitignore
```

---

## Модуль `jsonplaceholder_requests.py`

Модуль отвечает за получение данных из JSONPlaceholder.

Используются следующие API:

* `/users` — пользователи;
* `/posts` — публикации.

Для выполнения HTTP-запросов используется `aiohttp`.

Основная универсальная функция:

```python
async def fetch_json(url: str)
```

Она выполняет асинхронный GET-запрос и возвращает полученные JSON-данные.

Также реализованы функции:

```python
async def fetch_users_data()
async def fetch_posts_data()
```

Они получают данные пользователей и публикаций соответственно.

---

## Модуль `models.py`

Модуль содержит конфигурацию асинхронной работы SQLAlchemy и ORM-модели базы данных.

Для создания асинхронного подключения используется:

```python
create_async_engine()
```

Для работы с асинхронными сессиями используется:

```python
AsyncSession
```

### Модель `User`

Таблица:

```text
users
```

Поля:

* `id`
* `name`
* `username`
* `email`

У пользователя определена связь с публикациями:

```python
User.posts
```

### Модель `Post`

Таблица:

```text
posts
```

Поля:

* `id`
* `user_id`
* `title`
* `body`

Поле `user_id` является внешним ключом на:

```text
users.id
```

Для публикации определена связь:

```python
Post.user
```

Таким образом, между `User` и `Post` реализована связь один-ко-многим.

---

## Подключение к PostgreSQL

Строка подключения передаётся через переменную окружения:

```text
SQLALCHEMY_PG_CONN_URI
```

Пример:

```text
postgresql+asyncpg://postgres:password@localhost/postgres
```

Если переменная окружения не задана, приложение использует значение подключения по умолчанию, определённое в `models.py`.

---

## Модуль `main.py`

Модуль содержит основной асинхронный сценарий приложения.

Последовательность работы:

1. создаются необходимые таблицы базы данных;
2. одновременно запускаются запросы пользователей и публикаций;
3. полученные данные преобразуются в ORM-объекты;
4. пользователи добавляются в базу данных пакетно;
5. публикации добавляются в базу данных пакетно;
6. после каждой пакетной записи выполняется `commit`;
7. после завершения работы освобождаются ресурсы подключения к базе данных.

Для одновременного получения двух наборов данных используется:

```python
asyncio.gather(
    fetch_users_data(),
    fetch_posts_data(),
)
```

Полученные результаты передаются в функции добавления данных в БД.

---

## Установка зависимостей

Основные зависимости проекта устанавливаются командой:

```powershell
python -m pip install -r requirements.txt
```

Зависимости для разработки и тестирования устанавливаются командой:

```powershell
python -m pip install -r requirements-dev.txt
```

---

## Запуск проекта

После настройки подключения к PostgreSQL приложение запускается командой:

```powershell
python main.py
```

Для подключения к PostgreSQL можно задать переменную окружения:

```powershell
$env:SQLALCHEMY_PG_CONN_URI="postgresql+asyncpg://postgres:password@localhost/postgres"
```

После этого приложение использует указанную строку подключения.

---

## Тестирование

Для запуска тестов используется `pytest`.

Основная команда:

```powershell
pytest testing/test_homework.py -s -vv
```

Тесты проверяют:

* асинхронность функций HTTP-запросов;
* наличие и регистрацию ORM-моделей;
* необходимые поля модели `User`;
* необходимые поля модели `Post`;
* связи между `User` и `Post`;
* внешний ключ `Post.user_id`.

---

## Результат тестирования

Текущий набор тестов проходит успешно:

```text
6 passed
```

Проверяются следующие тесты:

```text
test_fetch_functions_are_async
test_models_are_registered
test_user_model_fields
test_post_model_fields
test_user_post_relationships
test_post_user_foreign_key
```

---

## GitHub Actions

Для автоматического запуска тестов используется workflow:

```text
.github/workflows/run_tests.yml
```

Workflow запускается при:

* `push`;
* `pull_request`.

В процессе выполнения:

1. загружается репозиторий;
2. устанавливается Python 3.13;
3. устанавливаются основные зависимости проекта;
4. устанавливаются зависимости для тестирования;
5. запускается `pytest`.

---

## Зависимости проекта

Основные зависимости находятся в файле:

```text
requirements.txt
```

Содержимое:

```text
aiohttp
SQLAlchemy>=1.4
asyncpg
```

Зависимости для разработки и тестирования находятся в файле:

```text
requirements-dev.txt
```

Содержимое:

```text
pytest
```

---

## Назначение проекта

Проект предназначен для практического применения асинхронного программирования в Python при одновременной работе с сетью и базой данных.

Основная цепочка обработки данных:

```text
JSONPlaceholder
      │
      ├── Users
      │
      └── Posts
            │
            ▼
          aiohttp
            │
            ▼
      asyncio.gather()
            │
            ▼
       Python data
            │
            ▼
        SQLAlchemy
            │
            ▼
        PostgreSQL
```

Проект содержит отдельные модули для HTTP-запросов, моделей базы данных, основного сценария приложения и автоматического тестирования.
