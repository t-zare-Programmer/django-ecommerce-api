from celery import shared_task
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_new_product(product_name):
    """
    Background workflow after creating a product.
    """

    print("=" * 60)
    print(f"Processing product: {product_name}")
    print("=" * 60)

    # 1) Clear cache
    cache.delete("active_products")

    print("Redis cache cleared.")

    # 2) Save log
    logger.info(f"Product '{product_name}' created successfully.")

    print("Log created.")

    # 3) Simulate sending email

    print(f"Email notification sent for '{product_name}'.")

    print("=" * 60)

    return f"{product_name} processed successfully."