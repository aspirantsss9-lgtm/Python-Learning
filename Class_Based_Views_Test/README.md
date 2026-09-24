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
* создание и редактирование товаров через формы;
* удаление товаров;
* серверную валидацию пользовательских данных;
* отображение ошибок формы в шаблоне;
* использование Class-Based Views;
* использование `ListView`, `DetailView`, `CreateView`, `UpdateView` и `DeleteView`;
* тестирование моделей, форм и представлений;
* тестирование CRUD-операций с использованием `pytest` и `pytest-django`.

---

## 1. Используемые технологии

* Python 3.13.14
* Django 6.1.1
* SQLite
* factory-boy
* Faker
* pytest
* pytest-django
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

* `name` — название товара;
* `description` — описание;
* `price` — цена;
* `created_at` — дата и время создания;
* `category` — категория товара.

Между `Product` и `Category` установлена связь `ForeignKey`.

---

## 4. Миграции

Для создания структуры базы данных используются стандартные Django migrations.

Создание миграций:

```powershell
python manage.py makemigrations
```

Применение миграций:

```powershell
python manage.py migrate
```

Проверка состояния миграций:

```powershell
python manage.py showmigrations
```

Файл первой миграции:

```text
store/migrations/0001_initial.py
```

Файл миграции должен храниться в репозитории.

---

## 5. Тестовые данные

Для генерации тестовых данных используются:

* `factory-boy`;
* `Faker`.

Файл:

```text
store/factories.py
```

Содержит:

* `CategoryFactory`;
* `ProductFactory`.

Для создания данных используется собственная команда Django:

```text
store/management/commands/create_data.py
```

### Создать 5 категорий и 20 товаров

```powershell
python manage.py create_data
```

### Создать только категории

Например, 5 категорий:

```powershell
python manage.py create_data --categories 5 --products 0
```

### Указать количество категорий и товаров

```powershell
python manage.py create_data --categories 10 --products 50
```

Команда проверяет, чтобы переданные количества не были отрицательными.

---

# 6. HTML-шаблоны

Шаблоны находятся в:

```text
store/templates/store/
```

Используется базовый шаблон:

```text
base.html
```

Другие страницы наследуют его с помощью:

```django
{% extends "store/base.html" %}
```

Содержимое страниц размещается в блоке:

```django
{% block content %}
{% endblock %}
```

Заголовок страницы также является отдельным блоком:

```django
{% block title %}
{% endblock %}
```

Таким образом, общая структура страницы хранится в `base.html`, а дочерние шаблоны содержат только специфическое содержимое.

---

## 7. Список товаров

Шаблон:

```text
store/templates/store/product_list.html
```

Страница отображает:

* название товара;
* описание;
* категорию;
* цену;
* ссылку на подробную информацию;
* ссылку на редактирование товара.

Также на странице доступна кнопка добавления нового товара.

Адрес:

```text
/products/
```

Главная страница приложения перенаправляет пользователя на список товаров.

Адрес:

```text
/
```

---

## 8. Детальная информация о товаре

Шаблон:

```text
store/templates/store/product_detail.html
```

На странице отображаются:

* ID товара;
* название;
* описание;
* цена;
* категория;
* дата создания.

Также доступны:

* переход к редактированию;
* возврат к списку товаров.

Адрес:

```text
/products/<id>/
```

Например:

```text
/products/1/
```

---

# 9. Добавление и редактирование товаров

Для работы с пользовательским вводом создана форма:

```text
store/forms.py
```

Используется:

```python
class ProductForm(forms.ModelForm):
```

Форма работает с моделью `Product`.

Поля формы:

* название;
* описание;
* цена;
* категория.

Форма используется как для создания нового товара, так и для редактирования существующего.

В текущей версии проекта форма используется совместно с Class-Based Views:

* `ProductCreateView`;
* `ProductUpdateView`.

---

## 10. Валидация формы

В `ProductForm` реализована дополнительная серверная валидация.

### Название

Название товара должно содержать минимум 3 символа.

Например:

```text
PC
```

не проходит дополнительную проверку.

### Цена

Цена должна быть больше нуля.

Например:

```text
0
```

не проходит проверку.

Ошибки валидации передаются обратно в шаблон и отображаются пользователю.

---

## 11. Шаблон формы

Для создания и редактирования используется общий шаблон:

```text
store/templates/store/product_form.html
```

Он получает от представления:

```text
form
page_title
submit_text
```

В случае ошибки пользовательские данные сохраняются в форме, а сообщения о валидации отображаются рядом с соответствующими полями.

Также обрабатываются общие ошибки формы через:

```django
{{ form.non_field_errors }}
```

Для POST-запросов используется CSRF-защита:

```django
{% csrf_token %}
```

---

# 12. Class-Based Views

Основная логика обработки страниц находится в:

```text
store/views.py
```

В текущей версии проекта вместо функциональных представлений используются Class-Based Views Django.

Реализованы следующие представления:

### `ProductListView`

Наследуется от:

```python
ListView
```

Отображает список всех товаров.

URL:

```text
/products/
```

Используемый шаблон:

```text
store/templates/store/product_list.html
```

---

### `ProductDetailView`

Наследуется от:

```python
DetailView
```

Отображает подробную информацию о выбранном товаре.

URL:

```text
/products/<id>/
```

Используемый шаблон:

```text
store/templates/store/product_detail.html
```

---

### `ProductCreateView`

Наследуется от:

```python
CreateView
```

Отвечает за создание нового товара.

Использует:

```text
store/forms.py
```

и шаблон:

```text
store/templates/store/product_form.html
```

URL:

```text
/products/add/
```

После успешного создания товара пользователь перенаправляется на страницу созданного товара.

---

### `ProductUpdateView`

Наследуется от:

```python
UpdateView
```

Отвечает за редактирование существующего товара.

Использует:

```text
store/forms.py
```

и общий шаблон:

```text
store/templates/store/product_form.html
```

URL:

```text
/products/<id>/edit/
```

После успешного сохранения пользователь перенаправляется на страницу товара.

---

### `ProductDeleteView`

Наследуется от:

```python
DeleteView
```

Отвечает за удаление существующего товара.

Для подтверждения удаления используется отдельный шаблон:

```text
store/templates/store/product_confirm_delete.html
```

URL:

```text
/products/<id>/delete/
```

После успешного удаления пользователь перенаправляется на список товаров.

Дополнительно выводится сообщение об успешном удалении товара.

---

## 13. URL-маршруты

Маршруты находятся в:

```text
config/urls.py
```

Основные адреса:

| URL                      | Представление       | Назначение               |
| ------------------------ | ------------------- | ------------------------ |
| `/`                      | `index`             | переход к списку товаров |
| `/products/`             | `ProductListView`   | список товаров           |
| `/products/<id>/`        | `ProductDetailView` | детальная информация     |
| `/products/add/`         | `ProductCreateView` | добавление товара        |
| `/products/<id>/edit/`   | `ProductUpdateView` | редактирование товара    |
| `/products/<id>/delete/` | `ProductDeleteView` | удаление товара          |
| `/admin/`                | Django Admin        | административная панель  |

Для Class-Based Views используется метод:

```python
.as_view()
```

Например:

```python
path(
    "products/",
    ProductListView.as_view(),
    name="product_list",
)
```

---

# 14. Удаление товара

Для подтверждения удаления используется шаблон:

```text
store/templates/store/product_confirm_delete.html
```

Перед удалением пользователю отображается название выбранного товара и предлагается подтвердить операцию.

Форма удаления использует POST-запрос:

```django
<form method="post">
    {% csrf_token %}
```

После подтверждения `ProductDeleteView` удаляет товар из базы данных.

После успешного удаления пользователь возвращается к списку товаров.

---

# 15. Административная панель

Настройка Django Admin находится в:

```text
store/admin.py
```

Для `Category` настроены:

* `list_display`;
* `search_fields`.

Для `Product` настроены:

* `list_display`;
* `search_fields`;
* `list_filter`.

Административная панель доступна по адресу:

```text
/admin/
```

---

# 16. Тестирование

Для тестирования проекта используются:

* `pytest`;
* `pytest-django`.

Зависимости находятся в:

```text
requirements.txt
```

Настройки pytest находятся в:

```text
pytest.ini
```

Файл содержит:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings
python_files = tests.py test_*.py *_tests.py
addopts = -ra
```

Тесты находятся в:

```text
store/tests.py
```

---

## 17. Тестирование CRUD модели

В тестах проверяются основные CRUD-операции с моделью `Product`:

### Create

Создание нового товара:

```python
Product.objects.create(...)
```

### Read

Получение товара из базы данных:

```python
Product.objects.get(pk=product.pk)
```

### Update

Изменение существующего товара и сохранение изменений:

```python
product.save()
```

### Delete

Удаление товара:

```python
product.delete()
```

Таким образом, проверяется полный жизненный цикл объекта `Product`.

Также отдельно проверяется CRUD для модели `Category`.

---

## 18. Тестирование форм

Проверяется корректная работа `ProductForm`.

Тестируются:

* корректное заполнение формы;
* отклонение слишком короткого названия;
* отклонение некорректной цены.

---

## 19. Тестирование Class-Based Views

В тестах проверяется работа основных CBV:

* `ProductListView`;
* `ProductDetailView`;
* `ProductCreateView`;
* `ProductUpdateView`;
* `ProductDeleteView`.

Также проверяется обработка некорректных данных при создании и редактировании товара.

Таким образом, тесты проверяют работу CRUD через Class-Based Views.

---

## 20. Запуск тестов

Для запуска всех тестов используется:

```powershell
pytest
```

В текущей версии проекта все тесты проходят успешно.

---

## 21. Проверка проекта

Для проверки конфигурации Django используется:

```powershell
python manage.py check
```

Ожидаемый результат:

```text
System check identified no issues (0 silenced).
```

---

## 22. Запуск проекта

Для запуска сервера разработки используется:

```powershell
python manage.py runserver
```

После запуска приложение доступно по адресу:

```text
http://127.0.0.1:8000/
```

Основная страница:

```text
http://127.0.0.1:8000/products/
```

