from decimal import Decimal

from django.contrib import admin
from django.http import HttpRequest

from .models import Category, Product


@admin.action(description="Увеличить цену на 10%%")
def increase_price_by_ten_percent(
    modeladmin: admin.ModelAdmin,
    request: HttpRequest,
    queryset,
) -> None:
    """Increase the price of selected products by 10%."""
    for product in queryset:
        product.price = (product.price * Decimal("1.10")).quantize(
            Decimal("0.01")
        )
        product.save(update_fields=["price"])


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for categories."""

    list_display = ("id", "name", "product_count")
    search_fields = ("name", "description")
    ordering = ("name",)

    @admin.display(description="Количество товаров")
    def product_count(self, obj: Category) -> int:
        return obj.products.count()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for products."""

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "created_at",
    )
    list_display_links = ("id", "name")
    list_filter = ("category", "created_at")
    search_fields = (
        "name",
        "description",
        "category__name",
    )
    ordering = ("-created_at",)
    list_per_page = 20
    date_hierarchy = "created_at"
    autocomplete_fields = ("category",)
    actions = (increase_price_by_ten_percent,)

