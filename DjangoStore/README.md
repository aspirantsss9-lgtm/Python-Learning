# DjangoStore

Учебный проект Django для работы с моделями, базой данных, ORM, миграциями, продвинутой настройкой административной панели Django, кастомными management-командами и фабриками для генерации тестовых данных.

## Цель проекта

Создать рабочий Django-проект с:

* подключённой базой данных SQLite;
* моделями `Category` и `Product`;
* связью `ForeignKey` между моделями;
* миграциями Django;
* работой с ORM;
* кастомной management-командой;
* фабриками `factory-boy`;
* генерацией данных с помощью Faker;
* продвинутой настройкой Django Admin;
* автоматическими тестами.

## Используемые технологии

* Python 3.13
* Django 6.1.1
* SQLite
* factory-boy
* Faker
* Django ORM
* Django Admin

## Структура проекта

```text
DjangoStore/
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── store/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── factories.py
    ├── models.py
    ├── tests.py
    ├── views.py
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    └── management/
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── create_data.py
```

## Создание виртуального окружения

Создание виртуального окружения:

```powershell
python -m venv .venv
```

Активация в PowerShell:

```powershell
.\.venv\Scripts\activate.ps1
```

Проверка Python:

```powershell
python --version
```

Проверка расположения Python:

```powershell
Get-Command python
```

Ожидается, что Python будет использоваться из:

```text
DjangoStore\.venv\Scripts\python.exe
```

## Установка зависимостей

Установка зависимостей из `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

Проверка версии Django:

```powershell
python -m django --version
```

## Проверка проекта

Перед созданием миграций можно выполнить:

```powershell
python manage.py check
```

Ожидаемый результат:

```text
System check identified no issues (0 silenced).
```

## Модели

В приложении `store` реализованы две модели.

### Category

Модель категории содержит:

* `name` — название категории;
* `description` — описание.

### Product

Модель товара содержит:

* `name` — название товара;
* `description` — описание;
* `price` — цена;
* `created_at` — дата создания;
* `category` — категория товара.

Между `Product` и `Category` установлена связь:

```text
Product → Category
```

Один товар относится к одной категории, а одна категория может содержать несколько товаров.

## Миграции

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

Для приложения `store` должна отображаться миграция:

```text
store
 [X] 0001_initial
```

## Работа с ORM

Запуск Django Shell:

```powershell
python manage.py shell
```

Пример получения количества категорий и товаров:

```python
from store.models import Category, Product

Category.objects.count()
Product.objects.count()
```

Получение категории товара:

```python
Product.objects.first().category
```

Получение товаров категории:

```python
Category.objects.first().products.count()
```

Выход из Shell:

```python
exit()
```

## Фабрики

Для генерации данных используются `factory-boy` и Faker.

В проекте реализованы:

* `CategoryFactory`;
* `ProductFactory`.

`CategoryFactory` создаёт категории с уникальными названиями.

`ProductFactory` создаёт товары и автоматически связывает их с категорией.

## Кастомная management-команда

В проекте реализована команда:

```powershell
python manage.py create_data
```

По умолчанию команда создаёт:

* 5 категорий;
* 20 товаров.

Можно указать собственное количество:

```powershell
python manage.py create_data --categories 3 --products 6
```

Например:

```powershell
python manage.py create_data --categories 2 --products 4
```

Ожидаемый результат:

```text
Created 2 categories and 4 products.
```

## Django Admin

Создание администратора:

```powershell
python manage.py createsuperuser
```

Запуск сервера:

```powershell
python manage.py runserver
```

Административная панель доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

В админке зарегистрированы:

* `Category`;
* `Product`.

### Настройка CategoryAdmin

Для категорий доступны:

* отображение количества товаров;
* поиск по названию и описанию;
* сортировка по названию.

В списке категорий отображается:

```text
ID
Название
Количество товаров
```

### Настройка ProductAdmin

Для товаров доступны:

* отображение основных полей;
* поиск по названию;
* поиск по описанию;
* поиск по названию категории;
* фильтрация по категории;
* фильтрация по дате создания;
* сортировка;
* навигация по датам;
* выбор категории через autocomplete;
* ограничение количества записей на странице.



