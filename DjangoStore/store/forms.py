from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """Form for creating and editing products."""

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "price",
            "category",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Название товара",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Описание товара",
                    "rows": 5,
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Цена",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_name(self) -> str:
        """Validate product name."""
        name = self.cleaned_data["name"].strip()

        if len(name) < 3:
            raise forms.ValidationError(
                "Название товара должно содержать минимум 3 символа."
            )

        return name

    def clean_price(self):
        """Validate product price."""
        price = self.cleaned_data["price"]

        if price <= 0:
            raise forms.ValidationError(
                "Цена товара должна быть больше нуля."
            )

        return price