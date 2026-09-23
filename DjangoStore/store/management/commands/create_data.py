from django.core.management.base import BaseCommand, CommandError

from store.factories import CategoryFactory, ProductFactory


class Command(BaseCommand):
    """Create sample store data using factories."""

    help = "Create sample categories and products."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--categories",
            type=int,
            default=5,
            help="Number of categories to create.",
        )
        parser.add_argument(
            "--products",
            type=int,
            default=20,
            help="Number of products to create.",
        )

    def handle(self, *args, **options) -> None:
        categories_count = options["categories"]
        products_count = options["products"]

        if categories_count < 0:
            raise CommandError("Categories count cannot be negative.")

        if products_count < 0:
            raise CommandError("Products count cannot be negative.")

        categories = CategoryFactory.create_batch(categories_count)

        if not categories and products_count > 0:
            categories = CategoryFactory.create_batch(1)

        for index in range(products_count):
            category = categories[index % len(categories)]
            ProductFactory.create(category=category)

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {categories_count} categories "
                f"and {products_count} products."
            )
        )