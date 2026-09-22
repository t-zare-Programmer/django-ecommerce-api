import pytest
from django.core.cache import cache

from apps.products.tasks import process_new_product


@pytest.mark.django_db
def test_process_new_product_clears_cache():
    cache.set("active_products", [1, 2, 3])

    result = process_new_product("iPhone 17")

    assert result == "iPhone 17 processed successfully."
    assert cache.get("active_products") is None
