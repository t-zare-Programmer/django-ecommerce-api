# seed_data.py
import os
import django
import random
from faker import Faker

# — تنظیم اولیه برای Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop_center.settings")
django.setup()

# مدل‌هایی که می‌خواهیم برای‌شان دیتا تولید کنیم
from apps.products.models import (
    Brand, ProductGroup, Feature, FeatureValue,
    Product, ProductGallery, ProductFeature
)

fake = Faker()

def seed_brands(n=5):
    brands = []
    for _ in range(n):
        b = Brand.objects.create(
            brand_title = fake.company(),
            slug = fake.slug(),
            image_name = None
        )
        brands.append(b)
    return brands

def seed_groups(n=5):
    groups = []
    for _ in range(n):
        g = ProductGroup.objects.create(
            group_title = fake.word().capitalize(),
            slug = fake.slug(),
            is_active = True,
            image_name = None,
            description = fake.text(max_nb_chars=100)
        )
        groups.append(g)
    return groups

def seed_features(n=5, groups=None):
    features = []
    for _ in range(n):
        f = Feature.objects.create(
            feature_name = fake.word().capitalize()
        )
        if groups:
            # نسبت تصادفی
            selected = random.sample(groups, k=random.randint(1, len(groups)))
            f.product_group.set(selected)
        features.append(f)
    return features

def seed_feature_values(features, per_feature=3):
    values = []
    for f in features:
        for _ in range(per_feature):
            fv = FeatureValue.objects.create(
                feature = f,
                value_title = fake.word().capitalize()
            )
            values.append(fv)
    return values

def seed_products(n=20, brands=None, groups=None, features=None):
    products = []
    for _ in range(n):
        brand = random.choice(brands) if brands else None
        p = Product.objects.create(
            product_name = fake.sentence(nb_words=3).rstrip('.'),
            summery_description = fake.text(max_nb_chars=100),
            description = fake.text(max_nb_chars=300),
            price = random.randint(1000, 100000),
            brand = brand,
            is_active = True,
            slug = fake.slug(),
            image_name = None
        )
        if groups:
            sel_groups = random.sample(groups, k=random.randint(1, len(groups)))
            p.product_group.set(sel_groups)
        # ویژگی‌ها نمونه ساده
        if features:
            # برای 1 تا 3 ویژگی به محصول نسبت بده
            sel_feats = random.sample(features, k=random.randint(1, min(3, len(features))))
            for f in sel_feats:

                ProductFeature.objects.create(
                    product = p,
                    feature = f,
                    value = fake.word().capitalize(),
                    filter_value = None
                )
        products.append(p)
    return products

def main():
    print("🔄 Clearing old data...")
    # حذف رکوردهای موجود
    ProductGallery.objects.all().delete()
    ProductFeature.objects.all().delete()
    Product.objects.all().delete()
    FeatureValue.objects.all().delete()
    Feature.objects.all().delete()
    ProductGroup.objects.all().delete()
    Brand.objects.all().delete()

    print("🎯 Seeding brands...")
    brands = seed_brands(5)
    print(f"{len(brands)} brands created.")

    print("🎯 Seeding product groups...")
    groups = seed_groups(5)
    print(f"{len(groups)} groups created.")

    print("🎯 Seeding features...")
    features = seed_features(5, groups=groups)
    print(f"{len(features)} features created.")

    #  تولید مقادیر برای ویژگی‌ها
    print("🎯 Seeding feature values...")
    seed_feature_values(features, per_feature=3)

    print("🎯 Seeding products...")
    seed_products(20, brands=brands, groups=groups, features=features)
    print("Products created.")

    print("✅ Seeding completed.")

if __name__ == "__main__":
    main()
