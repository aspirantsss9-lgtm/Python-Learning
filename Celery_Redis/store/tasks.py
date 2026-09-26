from __future__ import annotations

from celery import shared_task


@shared_task
def log_new_product(product_name: str) -> str:
    """Log information about a newly created product."""
    message = f"Новый товар добавлен: {product_name}"
    print(message)
    return message
