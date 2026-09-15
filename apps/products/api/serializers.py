from rest_framework import serializers

from ..models import (
    Brand,
    Product,
    ProductGallery,
    ProductGroup,
)
from apps.products.services.product_service import ProductService


# ============================================================
# BRAND
# ============================================================

class BrandSerializer(serializers.ModelSerializer):
    image_name = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Brand
        fields = [
            "id",
            "brand_title",
            "image_name",
            "slug",
        ]
        read_only_fields = [
            "id",
            "slug",
        ]


# ============================================================
# PRODUCT GROUP
# ============================================================

class ProductGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductGroup
        fields = [
            "id",
            "group_title",
            "slug",
        ]
        read_only_fields = [
            "id",
            "slug",
        ]


# ============================================================
# PRODUCT GALLERY
# ============================================================

class ProductGallerySerializer(serializers.ModelSerializer):
    image_name = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = ProductGallery
        fields = [
            "id",
            "image_name",
        ]
        read_only_fields = [
            "id",
        ]


# ============================================================
# PRODUCT
# ============================================================

class ProductSerializer(serializers.ModelSerializer):

    image_name = serializers.ImageField(
        required=False,
        allow_null=True,
    )

    brand = BrandSerializer(
        required=False,
        allow_null=True,
    )

    product_group = ProductGroupSerializer(
        many=True,
        required=False,
    )

    gallery_images = ProductGallerySerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = Product

        fields = [
            "id",
            "product_name",
            "summery_description",
            "description",
            "image_name",
            "price",
            "brand",
            "product_group",
            "gallery_images",
            "slug",
            "is_active",
        ]

        read_only_fields = [
            "id",
            "slug",
        ]

    # ========================================================
    # CREATE
    # ========================================================

    def create(self, validated_data):
        return ProductService.create_product(
            validated_data
        )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, instance, validated_data):
        return ProductService.update_product(
            instance,
            validated_data
        )