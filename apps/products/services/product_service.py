from apps.products.models import Product, Brand, ProductGroup, ProductGallery

class ProductService:

    @staticmethod
    def create_product(validated_data):
        brand_data = validated_data.pop('brand', None)
        groups_data = validated_data.pop('product_group', [])
        galleries_data = validated_data.pop('gallery_images', [])

        # brand
        if brand_data:
            brand, _ = Brand.objects.get_or_create(**brand_data)
            validated_data['brand'] = brand

        # create product
        product = Product.objects.create(**validated_data)

        # groups
        for group in groups_data:
            group_obj, _ = ProductGroup.objects.get_or_create(**group)
            product.product_group.add(group_obj)

        # gallery
        for gallery in galleries_data:
            ProductGallery.objects.create(product=product, **gallery)

        return product

    @staticmethod
    def update_product(instance, validated_data):
        brand_data = validated_data.pop('brand', None)
        groups_data = validated_data.pop('product_group', None)
        galleries_data = validated_data.pop('gallery_images', None)

        # brand
        if brand_data:
            brand, _ = Brand.objects.get_or_create(**brand_data)
            instance.brand = brand

        # groups
        if groups_data is not None:
            instance.product_group.clear()
            for group in groups_data:
                group_obj, _ = ProductGroup.objects.get_or_create(**group)
                instance.product_group.add(group_obj)

        # gallery
        if galleries_data is not None:
            instance.gallery_images.all().delete()
            for gallery in galleries_data:
                ProductGallery.objects.create(product=instance, **gallery)

        # other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance