from django.contrib import admin
from django.urls import path

from store.views import (
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    index,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", index, name="index"),

    path(
        "products/",
        ProductListView.as_view(),
        name="product_list",
    ),
    path(
        "products/add/",
        ProductCreateView.as_view(),
        name="product_create",
    ),
    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
    path(
        "products/<int:pk>/edit/",
        ProductUpdateView.as_view(),
        name="product_update",
    ),
    path(
        "products/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="product_delete",
    ),
]