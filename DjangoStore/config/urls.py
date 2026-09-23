from django.contrib import admin
from django.urls import path

from store.views import (
    index,
    product_create,
    product_detail,
    product_list,
    product_update,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("products/", product_list, name="product_list"),
    path(
        "products/<int:product_id>/",
        product_detail,
        name="product_detail",
    ),
    path(
        "products/add/",
        product_create,
        name="product_create",
    ),
    path(
        "products/<int:product_id>/edit/",
        product_update,
        name="product_update",
    ),
]