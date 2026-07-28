import factory
from apps.products.models import Brand
from apps.products.models import ProductGroup
from apps.products.models import Product


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    brand_title = factory.Sequence(lambda n: f"Brand {n}")
    slug = factory.Sequence(lambda n: f"brand-{n}")


class ProductGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductGroup

    group_title = factory.Sequence(lambda n: f"Group {n}")
    slug = factory.Sequence(lambda n: f"group-{n}")


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_name = factory.Sequence(lambda n: f"Product {n}")

    summery_description = "Summary"

    description = "Description"

    slug = factory.Sequence(lambda n: f"product-{n}")

    price = 1000

    is_active = True

    brand = factory.SubFactory(BrandFactory)