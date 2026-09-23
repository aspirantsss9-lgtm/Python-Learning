from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .factories import CategoryFactory, ProductFactory
from .forms import ProductForm
from .models import Category, Product


class CategoryModelTest(TestCase):
    """Test Category model."""

    def test_category_creation(self) -> None:
        category = CategoryFactory(name="Электроника")

        self.assertEqual(category.name, "Электроника")
        self.assertEqual(Category.objects.count(), 1)

    def test_category_string_representation(self) -> None:
        category = CategoryFactory(name="Книги")

        self.assertEqual(str(category), "Книги")


class ProductModelTest(TestCase):
    """Test Product model."""

    def test_product_creation(self) -> None:
        category = CategoryFactory(name="Ноутбуки")
        product = ProductFactory(
            name="Рабочий ноутбук",
            price=Decimal("1500.00"),
            category=category,
        )

        self.assertEqual(product.name, "Рабочий ноутбук")
        self.assertEqual(product.price, Decimal("1500.00"))
        self.assertEqual(product.category, category)

    def test_product_relationship(self) -> None:
        category = CategoryFactory(name="Телефоны")

        ProductFactory(category=category)
        ProductFactory(category=category)

        self.assertEqual(category.products.count(), 2)

    def test_product_string_representation(self) -> None:
        product = ProductFactory(name="Смартфон")

        self.assertEqual(str(product), "Смартфон")


class ProductFormTest(TestCase):
    """Test ProductForm validation."""

    def test_valid_form(self) -> None:
        category = CategoryFactory(name="Электроника")

        form = ProductForm(
            data={
                "name": "Ноутбук",
                "description": "Рабочий ноутбук",
                "price": "1500.00",
                "category": category.pk,
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_short_name(self) -> None:
        category = CategoryFactory(name="Электроника")

        form = ProductForm(
            data={
                "name": "PC",
                "description": "Описание",
                "price": "1500.00",
                "category": category.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_invalid_price(self) -> None:
        category = CategoryFactory(name="Электроника")

        form = ProductForm(
            data={
                "name": "Ноутбук",
                "description": "Описание",
                "price": "0",
                "category": category.pk,
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)


class ProductViewTest(TestCase):
    """Test product views."""

    def test_product_list(self) -> None:
        ProductFactory()

        response = self.client.get(reverse("product_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Список товаров")

    def test_product_detail(self) -> None:
        product = ProductFactory(name="Тестовый товар")

        response = self.client.get(
            reverse(
                "product_detail",
                kwargs={"product_id": product.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовый товар")

    def test_product_create(self) -> None:
        category = CategoryFactory(name="Электроника")

        response = self.client.post(
            reverse("product_create"),
            data={
                "name": "Новый товар",
                "description": "Описание нового товара",
                "price": "100.00",
                "category": category.pk,
            },
        )

        product = Product.objects.get(name="Новый товар")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "product_detail",
                kwargs={"product_id": product.pk},
            ),
        )

    def test_product_create_invalid_form(self) -> None:
        category = CategoryFactory(name="Электроника")

        response = self.client.post(
            reverse("product_create"),
            data={
                "name": "PC",
                "description": "Описание",
                "price": "0",
                "category": category.pk,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Название товара должно содержать минимум 3 символа.",
        )
        self.assertContains(
            response,
            "Цена товара должна быть больше нуля.",
        )

    def test_product_update(self) -> None:
        category = CategoryFactory(name="Электроника")
        product = ProductFactory(
            name="Старое название",
            price=Decimal("100.00"),
            category=category,
        )

        response = self.client.post(
            reverse(
                "product_update",
                kwargs={"product_id": product.pk},
            ),
            data={
                "name": "Новое название",
                "description": "Новое описание",
                "price": "250.00",
                "category": category.pk,
            },
        )

        product.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(product.name, "Новое название")
        self.assertEqual(product.price, Decimal("250.00"))