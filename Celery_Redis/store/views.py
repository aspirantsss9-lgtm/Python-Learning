from __future__ import annotations

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProductForm
from .models import Product
from .tasks import log_new_product


class ProductListView(ListView):
    """Display the list of all products."""

    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        """Return products with related categories loaded."""
        return Product.objects.select_related("category").all()


class ProductDetailView(DetailView):
    """Display detailed information about a product."""

    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        """Return products with related categories loaded."""
        return Product.objects.select_related("category").all()


class ProductCreateView(CreateView):
    """Create a new product and schedule a background task."""

    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"

    def get_context_data(self, **kwargs):
        """Add page-specific context to the template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Добавление товара"
        context["submit_text"] = "Добавить товар"
        return context

    def get_success_url(self):
        """Schedule a background task and return the product URL."""
        log_new_product.delay(self.object.name)
        return f"/products/{self.object.pk}/"


class ProductUpdateView(UpdateView):
    """Update an existing product."""

    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        """Add page-specific context to the template."""
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Редактирование товара"
        context["submit_text"] = "Сохранить изменения"
        return context

    def get_success_url(self):
        """Return the URL of the updated product."""
        return f"/products/{self.object.pk}/"


class ProductDeleteView(DeleteView):
    """Delete an existing product."""

    model = Product
    template_name = "store/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("product_list")

    def form_valid(self, form):
        """Delete the product and show a success message."""
        product_name = self.object.name
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Товар "{product_name}" успешно удалён.',
        )
        return response


def index(request):
    """Redirect the home page to the product list."""
    return redirect("product_list")