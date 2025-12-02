# seed_data_precise.py
import os
import django
import random
from faker import Faker
from django.utils.text import slugify
from datetime import datetime, timedelta
from django.utils import timezone

# تنظیم اولیه Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop_center.settings")
django.setup()

# ایمپورت مدل‌ها
from apps.products.models import Brand, ProductGroup, Feature, FeatureValue, Product, ProductFeature, ProductGallery
from apps.accounts.models import CustomUser, Customer
from apps.orders.models import Order, OrderDetails, PaymentType
from apps.discounts.models import Coupon, DiscountBasket, DiscountBasketDetails
from apps.warehouses.models import WarehouseType, Warehouse
from apps.payments.models import Payment

fake = Faker("en_US")  # می‌توان از 'fa_IR' هم استفاده کرد برای فارسی

# ------------------ برندها ------------------
def seed_brands(n=8):
    brands = []
    for _ in range(n):
        name = fake.company()
        slug = slugify(name)
        b = Brand.objects.create(
            brand_title=name,
            slug=slug,
            image_name=None
        )
        brands.append(b)
    return brands

# ------------------ گروه‌های محصول ------------------
def seed_groups(n=6):
    groups = []
    for _ in range(n):
        title = fake.word().capitalize()
        slug = slugify(title)
        g = ProductGroup.objects.create(
            group_title=title,
            slug=slug,
            is_active=True,
            description=fake.text(max_nb_chars=80),
            image_name=None
        )
        groups.append(g)
    return groups

# ------------------ ویژگی‌ها ------------------
def seed_features(n=5, groups=None):
    features = []
    for _ in range(n):
        f = Feature.objects.create(feature_name=fake.word().capitalize())
        if groups:
            selected = random.sample(groups, k=random.randint(1, len(groups)))
            f.product_group.set(selected)
        features.append(f)
    return features

# ------------------ مقادیر ویژگی ------------------
def seed_feature_values(features, per_feature=3):
    values = []
    for f in features:
        for _ in range(per_feature):
            fv = FeatureValue.objects.create(
                feature=f,
                value_title=fake.word().capitalize()
            )
            values.append(fv)
    return values

# ------------------ محصولات ------------------
def seed_products(n=120, brands=None, groups=None, features=None):
    products = []
    for _ in range(n):
        brand = random.choice(brands) if brands else None
        name = fake.sentence(nb_words=3).rstrip(".")
        slug = slugify(name)
        p = Product.objects.create(
            product_name=name,
            summery_description=fake.text(max_nb_chars=100),
            description=fake.text(max_nb_chars=300),
            price=random.randint(1000, 100000),
            brand=brand,
            is_active=True,
            slug=slug,
            image_name=None
        )
        # نسبت به گروه‌ها
        if groups:
            sel_groups = random.sample(groups, k=random.randint(1, min(2,len(groups))))
            p.product_group.set(sel_groups)
        # نسبت به ویژگی‌ها
        if features:
            sel_feats = random.sample(features, k=random.randint(1, min(3,len(features))))
            for f in sel_feats:
                ProductFeature.objects.create(
                    product=p,
                    feature=f,
                    value=fake.word().capitalize(),
                    filter_value=None
                )
        products.append(p)
    return products

# ------------------ کاربران ------------------
def seed_users(n=10):
    users = []
    for _ in range(n):
        mobile = fake.unique.msisdn()[:11]
        email = fake.email()
        name = fake.first_name()
        family = fake.last_name()
        password = "123456"
        user = CustomUser.objects.create_user(
            mobile_number=mobile,
            email=email,
            name=name,
            family=family,
            password=password,

        )
        Customer.objects.create(user=user)
        users.append(user)
    return users

# ------------------ انبارها ------------------
def seed_warehouses(products, users):
    types = [WarehouseType.objects.create(warehouse_type_title=t) for t in ["انبار اصلی","انبار فرعی"]]
    for p in products:
        for t in types:
            Warehouse.objects.create(
                warehouse_type=t,
                user_registered=random.choice(users),
                product=p,
                qty=random.randint(10, 200),
                price=p.price
            )

# ------------------ سفارش‌ها ------------------
def seed_orders(products, users):
    pt = PaymentType.objects.create(payment_title="Online")
    orders = []
    for _ in range(20):
        user = random.choice(users)
        order = Order.objects.create(
            customer=user.customer,
            is_finally=True,
            discount=random.randint(0,30)
        )
        for _ in range(random.randint(1,5)):
            product = random.choice(products)
            OrderDetails.objects.create(
                order=order,
                product=product,
                qty=random.randint(1,5),
                price=product.price
            )
        orders.append(order)
    return orders

# ------------------ کوپن‌ها و تخفیف‌ها ------------------
def seed_discounts(products):
    c = Coupon.objects.create(
        coupon_code="WELCOME10",
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=30),
        discount=10,
        is_active=True
    )
    d = DiscountBasket.objects.create(
        discount_title="تخفیف ویژه زمستان",
        start_date=timezone.now(),
        end_date=timezone.now()+timedelta(days=30),
        discount=15,
        is_active=True
    )
    for p in random.sample(products, k=min(10,len(products))):
        DiscountBasketDetails.objects.create(discount_basket=d, product=p)

# ------------------ اجرای کلی ------------------
def main():
    print("🔄 Clearing old data...")
    ProductGallery.objects.all().delete()
    ProductFeature.objects.all().delete()
    Product.objects.all().delete()
    FeatureValue.objects.all().delete()
    Feature.objects.all().delete()
    ProductGroup.objects.all().delete()
    Brand.objects.all().delete()
    Warehouse.objects.all().delete()
    WarehouseType.objects.all().delete()
    OrderDetails.objects.all().delete()
    Order.objects.all().delete()
    PaymentType.objects.all().delete()
    Coupon.objects.all().delete()
    DiscountBasketDetails.objects.all().delete()
    DiscountBasket.objects.all().delete()
    Customer.objects.all().delete()
    CustomUser.objects.filter(is_admin=False).delete()

    print("🎯 Seeding brands...")
    brands = seed_brands()
    print(f"{len(brands)} brands created.")

    print("🎯 Seeding product groups...")
    groups = seed_groups()
    print(f"{len(groups)} groups created.")

    print("🎯 Seeding features...")
    features = seed_features(groups=groups)
    print(f"{len(features)} features created.")

    print("🎯 Seeding feature values...")
    seed_feature_values(features)

    print("🎯 Seeding products...")
    products = seed_products(brands=brands, groups=groups, features=features)
    print(f"{len(products)} products created.")

    print("🎯 Seeding users...")
    users = seed_users()
    print(f"{len(users)} users created.")

    print("🎯 Seeding warehouses...")
    seed_warehouses(products, users)

    print("🎯 Seeding orders...")
    orders = seed_orders(products, users)
    print(f"{len(orders)} orders created.")

    print("🎯 Seeding discounts and coupons...")
    seed_discounts(products)

    print("✅ Seeding completed.")

if __name__ == "__main__":
    main()
