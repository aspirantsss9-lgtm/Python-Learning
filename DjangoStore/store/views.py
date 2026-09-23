from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def product_list(request: HttpRequest) -> HttpResponse:
    """Display the list of products."""
    products = Product.objects.select_related("category").all()

    return render(
        request,
        "store/product_list.html",
        {
            "products": products,
        },
    )


def product_detail(
    request: HttpRequest,
    product_id: int,
) -> HttpResponse:
    """Display product details."""
    product = get_object_or_404(
        Product.objects.select_related("category"),
        pk=product_id,
    )

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
        },
    )


def product_create(request: HttpRequest) -> HttpResponse:
    """Create a new product."""
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()
            return redirect("product_detail", product_id=product.pk)
    else:
        form = ProductForm()

    return render(
        request,
        "store/product_form.html",
        {
            "form": form,
            "page_title": "Добавление товара",
            "submit_text": "Добавить товар",
        },
    )


def product_update(
    request: HttpRequest,
    product_id: int,
) -> HttpResponse:
    """Edit an existing product."""
    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            product = form.save()
            return redirect("product_detail", product_id=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "store/product_form.html",
        {
            "form": form,
            "product": product,
            "page_title": "Редактирование товара",
            "submit_text": "Сохранить изменения",
        },
    )


def index(request: HttpRequest) -> HttpResponse:
    """Display the product list on the application root page."""
    return product_list(request)