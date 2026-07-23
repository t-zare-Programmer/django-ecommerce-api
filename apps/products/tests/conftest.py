import pytest
from rest_framework.test import APIClient
from apps.accounts.factories import UserFactory
from django.core.cache import cache
from apps.products.factories import (BrandFactory,ProductFactory,)


@pytest.fixture
def brand():
    return BrandFactory()


@pytest.fixture
def active_product(brand):
    return ProductFactory(
        brand=brand,
        is_active=True,
    )


@pytest.fixture
def inactive_product(brand):
    return ProductFactory(
        brand=brand,
        is_active=False,
    )


@pytest.fixture
def clear_cache():
    cache.clear()

    yield

    cache.clear()

@pytest.fixture
def product():

    return ProductFactory(
        product_name="iPhone 16",
        price=1000,
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def normal_user():
    return UserFactory()


@pytest.fixture
def admin_user():
    return UserFactory(
        is_admin=True,
    )


@pytest.fixture
def authenticated_user_client(normal_user):
    client = APIClient()
    client.force_authenticate(user=normal_user)
    return client


@pytest.fixture
def authenticated_admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


import pytest
from apps.accounts.factories import UserFactory


@pytest.fixture
def admin_user():
    return UserFactory(is_admin=True, is_active=True)


@pytest.fixture
def normal_user():
    return UserFactory(
        is_admin=False,
        is_active=True,
    )