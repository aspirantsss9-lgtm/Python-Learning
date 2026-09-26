from decimal import Decimal
from unittest.mock import patch

import pytest
from django.urls import reverse

from store.forms import ProductForm
from store.models import Category, Product
from store.tasks import log_new_product


@pytest.mark.django_db
def test_product_model_crud():
    """Test create, read, update, and delete operations for Product."""
    category = Category.objects.create(
        name="Test category",
        description="Test category description",
    )

    product = Product.objects.create(
        name="Test product",
        description="Test product description",
        price="100.00",
        category=category,
    )

    assert product.pk is not None
    assert Product.objects.get(pk=product.pk) == product
    assert product.name == "Test product"
    assert product.price == "100.00"
    assert product.category == category

    product.name = "Updated product"
    product.description = "Updated description"
    product.price = "150.00"
    product.save()

    updated_product = Product.objects.get(pk=product.pk)

    assert updated_product.name == "Updated product"
    assert updated_product.description == "Updated description"
    assert updated_product.price == Decimal("150.00")

    product_id = product.pk
    product.delete()

    assert not Product.objects.filter(pk=product_id).exists()


@pytest.mark.django_db
def test_category_crud():
    """Test create, read, update, and delete operations for Category."""
    category = Category.objects.create(
        name="Initial category",
        description="Initial description",
    )

    assert category.pk is not None
    assert Category.objects.get(pk=category.pk) == category

    category.name = "Updated category"
    category.description = "Updated description"
    category.save()

    updated_category = Category.objects.get(pk=category.pk)

    assert updated_category.name == "Updated category"
    assert updated_category.description == "Updated description"

    category_id = category.pk
    category.delete()

    assert not Category.objects.filter(pk=category_id).exists()


@pytest.mark.django_db
def test_product_form_valid():
    """Test that a valid product form is accepted."""
    category = Category.objects.create(name="Category")

    form = ProductForm(
        data={
            "name": "Test product",
            "description": "Test description",
            "price": "100.00",
            "category": category.pk,
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_product_form_rejects_short_name():
    """Test that a product name shorter than three characters is rejected."""
    category = Category.objects.create(name="Category")

    form = ProductForm(
        data={
            "name": "AB",
            "description": "Test description",
            "price": "100.00",
            "category": category.pk,
        }
    )

    assert not form.is_valid()
    assert "Название товара должно содержать минимум 3 символа." in (
        form.errors["name"]
    )


@pytest.mark.django_db
def test_product_form_rejects_invalid_price():
    """Test that a non-positive product price is rejected."""
    category = Category.objects.create(name="Category")

    form = ProductForm(
        data={
            "name": "Test product",
            "description": "Test description",
            "price": "0",
            "category": category.pk,
        }
    )

    assert not form.is_valid()
    assert "Цена товара должна быть больше нуля." in (
        form.errors["price"]
    )


@pytest.mark.django_db
def test_product_list_view(client):
    """Test the product list CBV."""
    category = Category.objects.create(name="Category")

    product = Product.objects.create(
        name="Test product",
        description="Description",
        price="100.00",
        category=category,
    )

    response = client.get(reverse("product_list"))

    assert response.status_code == 200
    assert product.name.encode() in response.content


@pytest.mark.django_db
def test_product_detail_view(client):
    """Test the product detail CBV."""
    category = Category.objects.create(name="Category")

    product = Product.objects.create(
        name="Test product",
        description="Description",
        price="100.00",
        category=category,
    )

    response = client.get(
        reverse(
            "product_detail",
            kwargs={"pk": product.pk},
        )
    )

    assert response.status_code == 200
    assert product.name.encode() in response.content


@pytest.mark.django_db
def test_product_create_view(client):
    """Test product creation and Celery task scheduling."""
    category = Category.objects.create(name="Category")

    with patch("store.views.log_new_product.delay") as mock_task:
        response = client.post(
            reverse("product_create"),
            data={
                "name": "New product",
                "description": "New description",
                "price": "200.00",
                "category": category.pk,
            },
        )

    assert response.status_code == 302

    product = Product.objects.get(name="New product")

    assert product.description == "New description"
    assert product.price == Decimal("200.00")
    assert product.category == category

    mock_task.assert_called_once_with("New product")


@pytest.mark.django_db
def test_product_update_view(client):
    """Test the product update CBV."""
    category = Category.objects.create(name="Category")

    product = Product.objects.create(
        name="Old product",
        description="Old description",
        price="100.00",
        category=category,
    )

    response = client.post(
        reverse(
            "product_update",
            kwargs={"pk": product.pk},
        ),
        data={
            "name": "Updated product",
            "description": "Updated description",
            "price": "150.00",
            "category": category.pk,
        },
    )

    assert response.status_code == 302

    product.refresh_from_db()

    assert product.name == "Updated product"
    assert product.description == "Updated description"
    assert product.price == Decimal("150.00")


@pytest.mark.django_db
def test_product_delete_view(client):
    """Test the product deletion CBV."""
    category = Category.objects.create(name="Category")

    product = Product.objects.create(
        name="Product to delete",
        description="Description",
        price="100.00",
        category=category,
    )

    response = client.post(
        reverse(
            "product_delete",
            kwargs={"pk": product.pk},
        )
    )

    assert response.status_code == 302
    assert not Product.objects.filter(pk=product.pk).exists()


@pytest.mark.django_db
def test_product_create_view_rejects_invalid_data(client):
    """Test that product creation rejects invalid form data."""
    category = Category.objects.create(name="Category")

    with patch("store.views.log_new_product.delay") as mock_task:
        response = client.post(
            reverse("product_create"),
            data={
                "name": "AB",
                "description": "Description",
                "price": "0",
                "category": category.pk,
            },
        )

    assert response.status_code == 200
    assert Product.objects.count() == 0
    mock_task.assert_not_called()


@pytest.mark.django_db
def test_product_update_view_rejects_invalid_data(client):
    """Test that product update rejects invalid form data."""
    category = Category.objects.create(name="Category")

    product = Product.objects.create(
        name="Old product",
        description="Old description",
        price="100.00",
        category=category,
    )

    response = client.post(
        reverse(
            "product_update",
            kwargs={"pk": product.pk},
        ),
        data={
            "name": "AB",
            "description": "Invalid",
            "price": "0",
            "category": category.pk,
        },
    )

    assert response.status_code == 200

    product.refresh_from_db()

    assert product.name == "Old product"
    assert product.description == "Old description"
    assert product.price == Decimal("100.00")


def test_log_new_product_task(capsys):
    """Test direct execution of the Celery task."""
    result = log_new_product.run("Test product")

    captured = capsys.readouterr()

    assert result == "Новый товар добавлен: Test product"
    assert "Новый товар добавлен: Test product" in captured.out