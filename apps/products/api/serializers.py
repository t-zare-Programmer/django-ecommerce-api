from rest_framework import serializers
from ..models import Product, Brand, ProductGroup, ProductGallery
from apps.products.services.product_service import ProductService

# -----------------------------------------------
# سریالایزر برند
class BrandSerializer(serializers.ModelSerializer):
    image_name = serializers.ImageField(required=False,allow_null=True)

    class Meta:
        model = Brand
        fields = ['id', 'brand_title', 'image_name', 'slug']

# -----------------------------------------------
# سریالایزر گروه محصول
class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ['id', 'group_title', 'slug']

# -----------------------------------------------
# سریالایزر تصاویر محصول
class ProductGallerySerializer(serializers.ModelSerializer):
    image_name = serializers.ImageField(required=False,allow_null=True)

    class Meta:
        model = ProductGallery
        fields = ['id', 'image_name']

# -----------------------------------------------
# سریالایزر اصلی محصول با قابلیت read & write
class ProductSerializer(serializers.ModelSerializer):
    image_name = serializers.ImageField(required=False,allow_null=True)

    # Nested serializers
    brand = BrandSerializer()
    product_group = ProductGroupSerializer(many=True)
    gallery_images = ProductGallerySerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'product_name',
            'summery_description',
            'description',
            'image_name',
            'price',
            'brand',
            'product_group',
            'gallery_images',
            'slug',
            'is_active',
        ]

    def create(self, validated_data):
        return ProductService.create_product(validated_data)

    def update(self, instance, validated_data):
        return ProductService.update_product(instance, validated_data)