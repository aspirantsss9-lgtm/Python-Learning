import factory
from faker import Faker

from .models import Category, Product


fake = Faker("ru_RU")


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory for creating Category objects."""

    class Meta:
        model = Category

    name = factory.LazyFunction(
        lambda: f"Категория {fake.unique.pyint(min_value=1, max_value=999999)}"
    )
    description = factory.LazyFunction(
        lambda: fake.text(max_nb_chars=150)
    )


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory for creating Product objects."""

    class Meta:
        model = Product

    name = factory.LazyFunction(
        lambda: f"Товар {fake.unique.pyint(min_value=1, max_value=999999)}"
    )
    description = factory.LazyFunction(
        lambda: fake.text(max_nb_chars=200)
    )
    price = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=10,
        max_value=9999,
    )
    category = factory.SubFactory(CategoryFactory)