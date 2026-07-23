import pytest
from rest_framework import status
from django.urls import reverse
from apps.products.factories import ProductFactory
from apps.products.models import Product


@pytest.mark.django_db
def test_product_list_api(
    api_client,
    active_product,
    inactive_product,
):

    url = reverse("api_products")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert response.data["success"] is True

    assert response.data["message"] == "Products retrieved successfully."

    results = response.data["data"]["results"]

    assert len(results) == 1

    assert results[0]["product_name"] == active_product.product_name

    assert results[0]["price"] == active_product.price

    assert results[0]["slug"] == active_product.slug


@pytest.mark.django_db
def test_product_detail_not_found(api_client):

    url = reverse(
        "api_product_detail",
        kwargs={
            "slug": "product-not-found"
        }
    )

    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

from django.core.cache import cache


@pytest.mark.django_db
def test_product_pagination(api_client):

    cache.clear()

    products = ProductFactory.create_batch(15)

    url = reverse("api_products")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert response.data["success"] is True

    assert response.data["message"] == "Products retrieved successfully."

    data = response.data["data"]

    assert data["count"] == 15

    assert data["previous"] is None

    assert data["next"] is not None

    assert len(data["results"]) == 5

    expected_products = sorted(
        products,
        key=lambda p: p.id,
        reverse=True
    )

    assert data["results"][0]["id"] == expected_products[0].id

    assert data["results"][0]["product_name"] == expected_products[0].product_name

    assert data["results"][-1]["id"] == expected_products[4].id


@pytest.mark.django_db
def test_product_pagination_second_page(api_client):

    cache.clear()

    products = ProductFactory.create_batch(15)

    url = reverse("api_products")

    response = api_client.get(
        url,
        {
            "page": 2
        }
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.data["data"]

    assert data["count"] == 15

    assert data["previous"] is not None

    assert data["next"] is not None

    assert len(data["results"]) == 5

    expected_products = sorted(
        products,
        key=lambda p: p.id,
        reverse=True
    )

    page2 = expected_products[5:10]

    assert data["results"][0]["id"] == page2[0].id

    assert data["results"][0]["product_name"] == page2[0].product_name

    assert data["results"][-1]["id"] == page2[-1].id


@pytest.mark.django_db
def test_product_search(api_client):

    cache.clear()

    ProductFactory(
        product_name="iPhone 17"
    )

    ProductFactory(
        product_name="Samsung S25"
    )

    url = reverse("api_products")

    response = api_client.get(
        url,
        {
            "search": "iphone"
        }
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.data["data"]

    assert data["count"] == 1

    assert len(data["results"]) == 1

    assert data["results"][0]["product_name"] == "iPhone 17"


@pytest.mark.django_db
def test_product_ordering_by_price(api_client):

    cache.clear()

    ProductFactory(
        product_name="Cheap",
        price=100
    )

    ProductFactory(
        product_name="Medium",
        price=500
    )

    ProductFactory(
        product_name="Expensive",
        price=1000
    )

    url = reverse("api_products")

    response = api_client.get(
        url,
        {
            "ordering": "price"
        }
    )

    assert response.status_code == status.HTTP_200_OK

    results = response.data["data"]["results"]

    assert results[0]["price"] == 100

    assert results[1]["price"] == 500

    assert results[2]["price"] == 1000


@pytest.mark.django_db
def test_product_ordering_by_price_desc(api_client):

    cache.clear()

    ProductFactory(
        product_name="Cheap",
        price=100
    )

    ProductFactory(
        product_name="Medium",
        price=500
    )

    ProductFactory(
        product_name="Expensive",
        price=1000
    )

    url = reverse("api_products")

    response = api_client.get(
        url,
        {
            "ordering": "-price"
        }
    )

    assert response.status_code == status.HTTP_200_OK

    results = response.data["data"]["results"]

    assert results[0]["price"] == 1000

    assert results[1]["price"] == 500

    assert results[2]["price"] == 100


@pytest.mark.django_db
def test_product_filter_by_brand(api_client):

    cache.clear()

    apple = ProductFactory(
        product_name="iPhone",
        brand__brand_title="Apple"
    )

    ProductFactory(
        product_name="Galaxy",
        brand__brand_title="Samsung"
    )

    url = reverse("api_products")

    response = api_client.get(
        url,
        {
            "brand__brand_title": "Apple"
        }
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.data["data"]

    assert data["count"] == 1

    assert len(data["results"]) == 1

    assert data["results"][0]["id"] == apple.id

    assert data["results"][0]["brand"]["brand_title"] == "Apple"


@pytest.mark.django_db
def test_create_product_requires_authentication(api_client):

    url = reverse("api_product_create")

    payload = {
        "product_name": "iPhone 17",
        "summery_description": "Summary",
        "description": "Description",
        "price": 1000,
        "brand": {
            "brand_title": "Apple"
        },
        "product_group": [],
        "gallery_images": [],
        "slug": "iphone17",
        "is_active": True,
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )

    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_create_product_api(api_client, admin_user):

    api_client.force_authenticate(user=admin_user)

    url = reverse("api_product_create")

    data = {
        "product_name": "iPhone 17",
        "price": 2500,
        "brand": {
            "brand_title": "Apple"
        },
        "product_group": [],
        "gallery_images": [],
    }

    api_client.raise_request_exception = True

    response = api_client.post(
        url,
        data,
        format="json",
    )

    print(response.status_code)

    try:
        print(response.data)
    except Exception:
        print(response.content)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_product_normal_user_forbidden(
    api_client,
    normal_user,
):

    api_client.force_authenticate(user=normal_user)

    url = reverse("api_product_create")

    data = {
        "product_name": "iPhone 17",
        "price": 2500,
        "brand": {
            "brand_title": "Apple"
        },
        "product_group": [],
        "gallery_images": [],
    }

    response = api_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_product_anonymous_forbidden(
    api_client,
):

    url = reverse("api_product_create")

    data = {
        "product_name": "iPhone 17",
        "price": 2500,
        "brand": {
            "brand_title": "Apple"
        },
        "product_group": [],
        "gallery_images": [],
    }

    response = api_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]


@pytest.mark.django_db
def test_update_product_api(
    api_client,
    admin_user,
):

    api_client.force_authenticate(user=admin_user)

    product = ProductFactory(
        product_name="Old Product",
        price=1000,
    )

    url = reverse(
        "api_product_update",
        kwargs={
            "slug": product.slug,
        }
    )

    data = {
        "product_name": "New Product",
        "price": 5000,
        "brand": {
            "brand_title": product.brand.brand_title,
        },
        "product_group": [],
        "gallery_images": [],
    }

    response = api_client.patch(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    product.refresh_from_db()

    assert product.product_name == "New Product"

    assert product.price == 5000


@pytest.mark.django_db
def test_update_product_normal_user_forbidden(
    api_client,
    normal_user,
):

    api_client.force_authenticate(user=normal_user)

    product = ProductFactory()

    url = reverse(
        "api_product_update",
        kwargs={
            "slug": product.slug,
        }
    )

    response = api_client.patch(
        url,
        {
            "product_name": "New Name",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_update_product_anonymous_forbidden(
    api_client,
):

    product = ProductFactory()

    url = reverse(
        "api_product_update",
        kwargs={
            "slug": product.slug,
        }
    )

    response = api_client.patch(
        url,
        {
            "product_name": "New Name",
        },
        format="json",
    )

    assert response.status_code in [
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    ]

@pytest.mark.django_db
def test_delete_product_api(api_client, admin_user):

    product = ProductFactory()

    api_client.force_authenticate(user=admin_user)

    url = reverse(
        "api_product_delete",
        kwargs={"slug": product.slug},
    )

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert Product.objects.filter(id=product.id).count() == 0

@pytest.mark.django_db
def test_delete_product_normal_user_forbidden(api_client, normal_user):

    product = ProductFactory()

    api_client.force_authenticate(user=normal_user)

    url = reverse(
        "api_product_delete",
        kwargs={"slug": product.slug},
    )

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert Product.objects.filter(id=product.id).exists()


@pytest.mark.django_db
def test_delete_product_anonymous_forbidden(api_client):

    product = ProductFactory()

    url = reverse(
        "api_product_delete",
        kwargs={"slug": product.slug},
    )

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    assert Product.objects.filter(id=product.id).exists()


@pytest.mark.django_db
def test_create_product_invalid_data(api_client, admin_user):

    api_client.force_authenticate(admin_user)

    url = reverse("api_product_create")

    response = api_client.post(
        url,
        {
            "price": 100
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_product_not_found(api_client, admin_user):

    api_client.force_authenticate(admin_user)

    url = reverse(
        "api_product_update",
        kwargs={"slug": "does-not-exist"},
    )

    response = api_client.put(
        url,
        {
            "product_name": "New Name",
            "price": 100,
            "brand": {
                "brand_title": "Apple"
            },
            "product_group": [],
            "gallery_images": [],
        },
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_product_not_found(api_client, admin_user):

    api_client.force_authenticate(admin_user)

    url = reverse(
        "api_product_delete",
        kwargs={"slug": "does-not-exist"},
    )

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND