import pytest
from django.core.cache import cache
from unittest.mock import patch

from apps.products.factories import ProductFactory
from apps.products.services.product_service import ProductService


# ==============================================================================================
@pytest.mark.django_db
def test_get_all_products():

    ProductFactory()

    products = ProductService.get_all_products()

    assert products.count() == 1


# ==============================================================================================
@pytest.mark.django_db
def test_get_active_products(
    active_product,
    inactive_product,
):

    products = ProductService.get_active_products()

    assert products.count() == 1
    assert products.first().product_name == active_product.product_name
# ==============================================================================================
@pytest.mark.django_db
def test_active_products_cached(
    clear_cache,
    active_product,
):

    ProductService.get_active_products()

    cached_products = cache.get(
        ProductService.ACTIVE_PRODUCTS_CACHE_KEY
    )

    assert cached_products is not None
# ==============================================================================================
@pytest.mark.django_db
def test_active_products_use_cache(
    clear_cache,
    active_product,
):

    ProductService.get_active_products()

    with patch(
        "apps.products.models.Product.objects.filter"
    ) as mocked_filter:

        ProductService.get_active_products()

        mocked_filter.assert_not_called()
# ==============================================================================================
@pytest.mark.django_db
def test_create_product():

    data = {
        "product_name": "iPhone 17",
        "price": 2500,
        "brand": {
            "brand_title": "Apple"
        },
        "product_group": [],
        "gallery_images": [],
    }

    product = ProductService.create_product(data)

    assert product.product_name == "iPhone 17"
    assert product.price == 2500
    assert product.brand.brand_title == "Apple"


# ==============================================================================================
@pytest.mark.django_db
def test_update_product(product):

    data = {
        "product_name": "iPhone 17",
        "price": 2500,
    }

    updated_product = ProductService.update_product(
        product,
        data,
    )

    assert updated_product.product_name == "iPhone 17"
    assert updated_product.price == 2500