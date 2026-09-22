import logging

from django.core.cache import cache
from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.products.models import (
    Brand,
    Product,
    ProductGallery,
    ProductGroup,
)
from apps.products.tasks import process_new_product


logger = logging.getLogger(__name__)


class ProductService:

    ACTIVE_PRODUCTS_CACHE_KEY = "active_products"
    ACTIVE_PRODUCTS_CACHE_TIMEOUT = 300

    @staticmethod
    def _clear_active_products_cache():
        cache.delete(ProductService.ACTIVE_PRODUCTS_CACHE_KEY)

    @staticmethod
    def _schedule_product_task(product_name):
        transaction.on_commit(
            lambda: process_new_product.delay(product_name)
        )

    # ============================================================
    # CREATE
    # ============================================================

    @staticmethod
    @transaction.atomic
    def create_product(validated_data):
        brand_data = validated_data.pop("brand", None)
        groups_data = validated_data.pop("product_group", [])
        galleries_data = validated_data.pop("gallery_images", [])

        # Brand
        if brand_data:
            brand, _ = Brand.objects.get_or_create(**brand_data)
            validated_data["brand"] = brand

        # Product
        product = Product.objects.create(**validated_data)

        # Product groups
        for group_data in groups_data:
            group, _ = ProductGroup.objects.get_or_create(**group_data)
            product.product_group.add(group)

        # Gallery
        for gallery_data in galleries_data:
            ProductGallery.objects.create(
                product=product,
                **gallery_data,
            )

        ProductService._clear_active_products_cache()

        # Execute Celery only after successful DB commit
        ProductService._schedule_product_task(product.product_name)

        logger.info(
            "Product created successfully: id=%s name=%s",
            product.id,
            product.product_name,
        )

        return product

    # ============================================================
    # UPDATE
    # ============================================================

    @staticmethod
    @transaction.atomic
    def update_product(instance, validated_data):
        brand_data = validated_data.pop("brand", None)
        groups_data = validated_data.pop("product_group", None)
        galleries_data = validated_data.pop("gallery_images", None)

        # Brand
        if brand_data is not None:
            brand, _ = Brand.objects.get_or_create(**brand_data)
            instance.brand = brand

        # Product groups
        if groups_data is not None:
            instance.product_group.clear()

            for group_data in groups_data:
                group, _ = ProductGroup.objects.get_or_create(**group_data)
                instance.product_group.add(group)

        # Gallery
        if galleries_data is not None:
            instance.gallery_images.all().delete()

            for gallery_data in galleries_data:
                ProductGallery.objects.create(
                    product=instance,
                    **gallery_data,
                )

        # Other product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        ProductService._clear_active_products_cache()

        # Execute Celery only after successful DB commit
        ProductService._schedule_product_task(instance.product_name)

        logger.info(
            "Product updated successfully: id=%s name=%s",
            instance.id,
            instance.product_name,
        )

        return instance

    # ============================================================
    # READ
    # ============================================================

    @staticmethod
    def get_active_products():
        """
        Return active products as a QuerySet.

        Important:
        DRF filtering, searching, ordering and pagination
        require a QuerySet, not a cached list.
        """

        cached_ids = cache.get(
            ProductService.ACTIVE_PRODUCTS_CACHE_KEY
        )

        if cached_ids is None:
            logger.info("Active products loaded from database.")

            cached_ids = list(
                Product.objects
                .filter(is_active=True)
                .order_by("-id")
                .values_list("id", flat=True)
            )

            cache.set(
                ProductService.ACTIVE_PRODUCTS_CACHE_KEY,
                cached_ids,
                timeout=ProductService.ACTIVE_PRODUCTS_CACHE_TIMEOUT,
            )

        else:
            logger.info("Active product IDs loaded from Redis.")

        if not cached_ids:
            return Product.objects.none()

        return (
            Product.objects
            .filter(
                id__in=cached_ids,
                is_active=True,
            )
            .order_by("-id")
        )

    @staticmethod
    def get_all_products():
        """
        Return all products.

        Used by admin-only CRUD operations such as
        update and delete.
        """
        return Product.objects.all()
    # ============================================================
    # DELETE
    # ============================================================

    @staticmethod
    @transaction.atomic
    def delete_product(instance):
        product_id = instance.id
        product_name = instance.product_name

        instance.delete()

        ProductService._clear_active_products_cache()

        logger.info(
            "Product deleted successfully: id=%s name=%s",
            product_id,
            product_name,
        )

    # ============================================================
    # HELPERS
    # ============================================================

    @staticmethod
    def get_product_or_404(slug):
        return get_object_or_404(
            Product,
            slug=slug,
        )