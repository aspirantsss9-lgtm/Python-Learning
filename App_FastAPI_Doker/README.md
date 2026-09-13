# FastAPI Docker

## Описание проекта

FastAPI Docker — учебное веб-приложение на Python с использованием FastAPI, подготовленное для запуска в Docker-контейнере.

Проект демонстрирует:

* создание веб-приложения на FastAPI;
* создание HTTP-эндпоинтов;
* работу с HTML-шаблонами Jinja2;
* подключение статических файлов;
* создание API;
* создание Docker-образа;
* установку зависимостей внутри Docker-контейнера;
* запуск веб-сервера Uvicorn внутри контейнера.

Основная задача текущего проекта — подготовить FastAPI-приложение к контейнеризации с помощью Docker.

---

## Используемые технологии

* Python 3.13
* FastAPI
* Uvicorn
* Jinja2
* Bootstrap 5
* Docker
* Docker Desktop

---

## Структура проекта

```text
App_FastAPI_Doker/
│
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── books.py
│   │   └── pages.py
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   ├── templates/
│   │   ├── about.html
│   │   ├── base.html
│   │   └── index.html
│   │
│   ├── __init__.py
│   └── app.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

---

## Основные маршруты

### Главная страница

```text
GET /
```

Открывает главную страницу приложения.

Адрес:

```text
http://127.0.0.1:8000/
```

### Страница About

```text
GET /about/
```

Открывает информационную страницу приложения.

Адрес:

```text
http://127.0.0.1:8000/about/
```

### Проверка работы приложения

```text
GET /ping/
```

Возвращает JSON:

```json
{
    "message": "pong"
}
```

Адрес:

```text
http://127.0.0.1:8000/ping/
```

Этот маршрут используется для проверки того, что FastAPI-приложение успешно запущено.

### API книг

Получение списка книг:

```text
GET /api/books/
```

Получение книги по идентификатору:

```text
GET /api/books/{book_id}/
```

Создание книги:

```text
POST /api/books/
```

Пример данных для создания книги:

```json
{
    "title": "The Hobbit",
    "author": "J.R.R. Tolkien",
    "year": 1937
}
```

---

## Локальный запуск приложения

### 1. Создание виртуального окружения

В корне проекта:

```powershell
python -m venv .venv
```

### 2. Активация виртуального окружения

Для PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

После активации в терминале появится:

```text
(.venv)
```

### 3. Установка зависимостей

```powershell
python -m pip install -r requirements.txt
```

### 4. Запуск приложения

```powershell
python -m uvicorn app.app:app --reload
```

После запуска приложение доступно по адресу:

```text
http://127.0.0.1:8000/
```

Проверка:

```text
http://127.0.0.1:8000/ping/
```

Ожидаемый результат:

```json
{
    "message": "pong"
}
```

---

## Документация FastAPI

FastAPI автоматически предоставляет интерактивную документацию Swagger.

Адрес:

```text
http://127.0.0.1:8000/docs
```

Также доступна альтернативная документация ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

## Запуск в Docker

Для запуска приложения в Docker используется `Dockerfile`.

### Сборка Docker-образа

В корне проекта выполнить:

```powershell
docker build -t app-fastapi .
```

Команда создаёт Docker-образ с именем:

```text
app-fastapi
```

Во время сборки:

1. используется базовый образ Python;
2. устанавливаются зависимости из `requirements.txt`;
3. копируется код приложения;
4. объявляется порт `8000`;
5. задаётся команда запуска Uvicorn.

### Запуск контейнера

После успешной сборки:

```powershell
docker run -d -p 8000:8000 --name app-fastapi-container app-fastapi
```

Параметры команды:

* `-d` — запуск контейнера в фоновом режиме;
* `-p 8000:8000` — подключение порта компьютера 8000 к порту контейнера 8000;
* `--name app-fastapi-container` — имя контейнера;
* `app-fastapi` — имя Docker-образа.

После запуска приложение доступно по адресу:

```text
http://127.0.0.1:8000/
```

Проверка Docker-контейнера:

```text
http://127.0.0.1:8000/ping/
```

Ожидаемый ответ:

```json
{
    "message": "pong"
}
```

---

## Проверка контейнера

Список запущенных контейнеров:

```powershell
docker ps
```

Просмотр логов:

```powershell
docker logs app-fastapi-container
```

Остановка контейнера:

```powershell
docker stop app-fastapi-container
```

Повторный запуск:

```powershell
docker start app-fastapi-container
```

Удаление контейнера:

```powershell
docker rm app-fastapi-container
```

---

## Переменные и зависимости

Зависимости проекта находятся в файле:

```text
requirements.txt
```

Содержимое файла:

```text
fastapi
uvicorn[standard]
jinja2
```

Локальное виртуальное окружение `.venv` не добавляется в репозиторий и не копируется в Docker-образ.

---

## Dockerfile

Dockerfile находится в корне проекта и отвечает за создание Docker-образа приложения.

Основные этапы:

```text
Python image
     ↓
WORKDIR /app
     ↓
COPY requirements.txt
     ↓
Установка зависимостей
     ↓
COPY приложения
     ↓
EXPOSE 8000
     ↓
Запуск Uvicorn
```

Приложение запускается внутри контейнера на:

```text
0.0.0.0:8000
```

---

## Игнорируемые файлы

Для Git используется файл:

```text
.gitignore
```

Он исключает из репозитория служебные файлы и каталоги, например:

```text
.venv/
.idea/
__pycache__/
```

Для Docker используется файл:

```text
.dockerignore
```

Он предотвращает передачу ненужных файлов в Docker-контекст сборки.

---

## Результат

В результате выполнения задания создано FastAPI-приложение, которое:

* запускается локально через Uvicorn;
* предоставляет маршрут `/ping/`;
* возвращает `{"message": "pong"}`;
* имеет API для работы с книгами;
* использует HTML-шаблоны Jinja2;
* использует статические файлы;
* имеет Dockerfile;
* устанавливает зависимости при сборке Docker-образа;
* запускает Uvicorn внутри Docker-контейнера на порту `8000`.
