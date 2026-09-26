# DjangoStore

Учебное веб-приложение интернет-магазина на Django.

Проект создан в рамках домашних заданий по Django и демонстрирует:

* работу с моделями и связями между ними;
* работу с Django ORM;
* использование миграций;
* создание тестовых данных через `factory-boy` и Faker;
* создание собственной management-команды;
* настройку административной панели Django;
* работу с HTML-шаблонами;
* наследование шаблонов через `extends` и `block`;
* передачу данных из представлений в шаблоны;
* создание, редактирование и удаление товаров через формы;
* серверную валидацию пользовательских данных;
* отображение ошибок формы в шаблоне;
* использование Class-Based Views;
* использование `ListView`, `DetailView`, `CreateView`, `UpdateView` и `DeleteView`;
* тестирование моделей, форм и представлений;
* тестирование CRUD-операций с использованием `pytest` и `pytest-django`;
* выполнение фоновых задач с использованием Celery;
* использование Redis в качестве брокера сообщений и backend результатов.

---

## 1. Используемые технологии

* Python 3.13.14
* Django 6.1.1
* SQLite
* factory-boy
* Faker
* pytest
* pytest-django
* Celery
* Redis
* HTML
* CSS
* Django Templates
* Django Class-Based Views

---

## 2. Структура проекта

```text
DjangoStore/
├── .gitignore
├── README.md
├── pytest.ini
├── requirements.txt
├── manage.py
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── store/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── factories.py
    ├── forms.py
    ├── models.py
    ├── tasks.py
    ├── tests.py
    ├── views.py
    │
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    │
    ├── management/
    │   ├── __init__.py
    │   └── commands/
    │       ├── __init__.py
    │       └── create_data.py
    │
    └── templates/
        └── store/
            ├── base.html
            ├── product_list.html
            ├── product_detail.html
            ├── product_form.html
            └── product_confirm_delete.html
```

---

## 3. Модели

Приложение `store` содержит две основные модели.

### Category

Модель категории товара содержит:

* `name` — название категории;
* `description` — описание категории.

Название категории должно быть уникальным.

### Product

Модель товара содержит:

* `name` — название;
* `description` — описание;
* `price` — цена;
* `created_at` — дата и время создания;
* `category` — категория товара.

Между `Product` и `Category` установлена связь `ForeignKey`.

---

## 4. Миграции

Основная миграция:

```text
store/migrations/0001_initial.py
```

Она создаёт модели:

```text
Category
Product
```

Миграция должна находиться в Git.

---

## 5. Фабрики

Для генерации тестовых данных используются:

```text
factory-boy
Faker
```

Файл:

```text
store/factories.py
```

В проекте используются:

```text
CategoryFactory
ProductFactory
```

`ProductFactory` автоматически создаёт связанную категорию через `SubFactory`.

---

## 6. Кастомная management-команда

Файл:

```text
store/management/commands/create_data.py
```

Команда:

```powershell
python manage.py create_data
```

По умолчанию создаёт тестовые категории и товары.

Количество объектов можно задавать параметрами:

```powershell
python manage.py create_data --categories 3 --products 6
```

---

## 7. Django Admin

Административная панель настроена в:

```text
store/admin.py
```

Зарегистрированы:

```text
Category
Product
```

Настроены отображение данных, поиск, фильтрация, сортировка и другие возможности административной панели.

Адрес:

```text
http://127.0.0.1:8000/admin/
```

---

## 8. HTML-шаблоны

Шаблоны находятся в:

```text
store/templates/store/
```

Используется базовый шаблон:

```text
base.html
```

Остальные страницы наследуют его с помощью:

```django
{% extends "store/base.html" %}
```

Реализованы страницы:

* списка товаров;
* детальной информации о товаре;
* создания товара;
* редактирования товара;
* подтверждения удаления товара.

---

## 9. Формы

Файл:

```text
store/forms.py
```

Используется `ProductForm` на основе `ModelForm`.

Форма применяется для:

* создания товара;
* редактирования товара.

Реализована серверная валидация:

* название товара должно содержать минимум 3 символа;
* цена должна быть больше нуля.

Ошибки формы отображаются непосредственно в HTML-шаблоне.

---

## 10. Class-Based Views

В файле:

```text
store/views.py
```

используются generic Class-Based Views Django:

```text
ProductListView
ProductDetailView
ProductCreateView
ProductUpdateView
ProductDeleteView
```

Используются:

```text
ListView
DetailView
CreateView
UpdateView
DeleteView
```

### ProductListView

Отображает список всех товаров.

Используется:

```text
/products/
```

### ProductDetailView

Отображает подробную информацию о выбранном товаре.

Используется:

```text
/products/<id>/
```

### ProductCreateView

Создаёт новый товар с использованием `ProductForm`.

Используется:

```text
/products/add/
```

### ProductUpdateView

Редактирует существующий товар.

Используется:

```text
/products/<id>/edit/
```

### ProductDeleteView

Удаляет существующий товар после подтверждения.

Используется:

```text
/products/<id>/delete/
```

Для удаления используется отдельный шаблон:

```text
store/templates/store/product_confirm_delete.html
```

---

## 11. URL-маршруты

Основные маршруты:

| URL                      | Представление       | Назначение               |
| ------------------------ | ------------------- | ------------------------ |
| `/`                      | `index`             | переход к списку товаров |
| `/products/`             | `ProductListView`   | список товаров           |
| `/products/<id>/`        | `ProductDetailView` | информация о товаре      |
| `/products/add/`         | `ProductCreateView` | добавление товара        |
| `/products/<id>/edit/`   | `ProductUpdateView` | редактирование товара    |
| `/products/<id>/delete/` | `ProductDeleteView` | удаление товара          |
| `/admin/`                | Django Admin        | административная панель  |

Для подключения Class-Based Views используется:

```python
.as_view()
```

---

## 12. ORM и CRUD

Работа с моделями выполняется через Django ORM.

Основные CRUD-операции:

### Create

```python
Product.objects.create(...)
```

### Read

```python
Product.objects.get(pk=product.pk)
```

### Update

```python
product.save()
```

### Delete

```python
product.delete()
```

Также проверяется связь между `Product` и `Category`.

---

## 13. Тестирование

Тесты находятся в:

```text
store/tests.py
```

Для запуска используется:

```powershell
pytest
```

В тестах проверяются:

* CRUD модели `Product`;
* CRUD модели `Category`;
* корректная работа `ProductForm`;
* валидация названия товара;
* валидация цены;
* `ProductListView`;
* `ProductDetailView`;
* `ProductCreateView`;
* `ProductUpdateView`;
* `ProductDeleteView`;
* обработка некорректных данных;
* интеграция создания товара с постановкой Celery-задачи;
* выполнение Celery-задачи напрямую.

---

## 14. Проверка проекта

Для проверки конфигурации Django используется:

```powershell
python manage.py check
```

Текущий результат:

```text
System check identified no issues (0 silenced).
```

---

## 15. Запуск проекта

Активировать виртуальное окружение:

```powershell
.\.venv\Scripts\activate.ps1
```

Проверить Python:

```powershell
python --version
```

Установить зависимости:

```powershell
python -m pip install -r requirements.txt
```

Применить миграции:

```powershell
python manage.py migrate
```

Создать тестовые данные:

```powershell
python manage.py create_data
```

Запустить тесты:

```powershell
pytest
```

Проверить Django:

```powershell
python manage.py check
```

Запустить сервер:

```powershell
python manage.py runserver
```

---

# 16. Celery и Redis

В рамках текущего ДЗ в проект добавлена поддержка фоновых задач с использованием Celery.

Цель:

* настроить Celery;
* использовать Redis как брокер сообщений;
* создать фоновую задачу;
* запускать задачу при добавлении нового товара;
* проверить постановку задачи в тестах.

---

## 16.1. Зависимости Celery

В `requirements.txt` добавлены:

```text
celery
redis
```

Полный список зависимостей включает:

```text
Django==6.1.1
factory-boy
Faker
pytest
pytest-django
celery
redis
```

---

## 16.2. Конфигурация Celery

Создан файл:

```text
config/celery.py
```

Celery-приложение создаётся следующим образом:

```python
app = Celery("djangostore")
```

Настройки Celery загружаются из Django:

```python
app.config_from_object("django.conf:settings", namespace="CELERY")
```

Задачи приложений автоматически обнаруживаются:

```python
app.autodiscover_tasks()
```

---

## 16.3. Настройка Redis

В `config/settings.py` настроены Redis broker и backend:

```python
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
```

Также настроена работа с JSON:

```python
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
```

Часовой пояс Celery соответствует настройкам Django:

```python
CELERY_TIMEZONE = TIME_ZONE
```

---

## 16.4. Фоновая задача

Задача находится в:

```text
store/tasks.py
```

Реализована задача:

```text
log_new_product
```

Она получает название нового товара и выводит сообщение:

```text
Новый товар добавлен: <название товара>
```

Задача объявлена с помощью:

```python
@shared_task
```

Результатом выполнения задачи является сформированное сообщение.

---

## 16.5. Постановка задачи при создании товара

В `ProductCreateView` после успешного создания товара вызывается Celery-задача:

```python
log_new_product.delay(self.object.name)
```

Таким образом, создание товара приводит к постановке фоновой задачи в Celery.

Используется именно асинхронный вызов:

```python
.delay(...)
```

---

## 16.6. Тестирование Celery-задачи

В тестах проверяется вызов задачи при создании товара.

Проверяется, что:

```python
log_new_product.delay(...)
```

вызывается один раз и получает название созданного товара.

Также отдельно проверяется сама задача:

```python
log_new_product.run("Test product")
```

Проверяется:

* возвращаемое значение;
* вывод сообщения;
* корректное название товара в сообщении.

---

# 19. Текущий статус проекта

Проект `DjangoStore` содержит реализованные возможности предыдущих домашних заданий:

* модели `Category` и `Product`;
* связь `ForeignKey`;
* миграции;
* Django ORM;
* фабрики `factory-boy`;
* Faker;
* management-команду;
* Django Admin;
* HTML-шаблоны;
* формы и валидацию;
* Class-Based Views;
* CRUD-операции;
* тестирование с `pytest` и `pytest-django`.

