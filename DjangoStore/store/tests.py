from decimal import Decimal

from django.test import TestCase

from .factories import CategoryFactory, ProductFactory
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