from rest_framework import serializers
from ..models import Product, Brand, ProductGroup, ProductGallery

# -----------------------------------------------
# سریالایزر برند
class BrandSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = ProductGallery
        fields = ['id', 'image_name']

# -----------------------------------------------
# سریالایزر اصلی محصول با قابلیت read & write
class ProductSerializer(serializers.ModelSerializer):
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

    # برای write کردن nested fields باید override کنیم
    def create(self, validated_data):
        brand_data = validated_data.pop('brand', None)
        groups_data = validated_data.pop('product_group', [])
        galleries_data = validated_data.pop('gallery_images', [])

        # اگر برند داده شد
        if brand_data:
            brand, created = Brand.objects.get_or_create(**brand_data)
            validated_data['brand'] = brand

        # ایجاد محصول
        product = Product.objects.create(**validated_data)

        # افزودن گروه‌ها
        for group in groups_data:
            group_obj, created = ProductGroup.objects.get_or_create(**group)
            product.product_group.add(group_obj)

        # افزودن تصاویر
        for gallery in galleries_data:
            ProductGallery.objects.create(product=product, **gallery)

        return product

    # آپدیت محصول
    def update(self, instance, validated_data):
        brand_data = validated_data.pop('brand', None)
        groups_data = validated_data.pop('product_group', None)
        galleries_data = validated_data.pop('gallery_images', None)

        # بروزرسانی برند
        if brand_data:
            brand, created = Brand.objects.get_or_create(**brand_data)
            instance.brand = brand

        # بروزرسانی گروه‌ها
        if groups_data is not None:
            instance.product_group.clear()
            for group in groups_data:
                group_obj, created = ProductGroup.objects.get_or_create(**group)
                instance.product_group.add(group_obj)

        # بروزرسانی تصاویر
        if galleries_data is not None:
            instance.gallery_images.all().delete()
            for gallery in galleries_data:
                ProductGallery.objects.create(product=instance, **gallery)

        # بروزرسانی بقیه فیلدها
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
