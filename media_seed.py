import os
import random
from django.core.files import File
from django.conf import settings

from apps.products.models import Brand, ProductGroup, Product, ProductGallery

# ===============================
# مسیر اصلی که تصاویر در آن قرار دارند
# ===============================
MEDIA_SEED = os.path.join(settings.MEDIA_ROOT, 'images')

# مسیر عکس پیش‌فرض
DEFAULT_IMAGE = os.path.join(MEDIA_SEED, 'default.jpg')

# مسیر هر پوشه
BRAND_PATH = os.path.join(MEDIA_SEED, 'brand')
GROUP_PATH = os.path.join(MEDIA_SEED, 'product_group')
PRODUCT_PATH = os.path.join(MEDIA_SEED, 'product')
GALLERY_PATH = os.path.join(MEDIA_SEED, 'product_gallery')


# ===============================
# تابع کمکی برای پیدا کردن یا جایگزینی تصویر
# ===============================
def get_image_or_default(path):
    """اگر عکس موجود نبود default.jpg داده می‌شود."""
    if os.path.exists(path):
        return path
    return DEFAULT_IMAGE


# ===============================
# برندها
# ===============================
print("🔄 Updating brands images...")

for brand in Brand.objects.all():
    file_path = os.path.join(BRAND_PATH, f"{brand.id}.jpg")
    file_path = get_image_or_default(file_path)

    with open(file_path, "rb") as f:
        brand.image_name.save(f"{brand.id}.jpg", File(f), save=True)

print("✅ Brands updated!")


# ===============================
# گروه محصولات
# ===============================
print("🔄 Updating product groups images...")

for group in ProductGroup.objects.all():
    file_path = os.path.join(GROUP_PATH, f"{group.id}.jpg")
    file_path = get_image_or_default(file_path)

    with open(file_path, "rb") as f:
        group.image_name.save(f"{group.id}.jpg", File(f), save=True)

print("✅ Product groups updated!")


# ===============================
# محصولات
# ===============================
print("🔄 Updating products images...")

for product in Product.objects.all():
    file_path = os.path.join(PRODUCT_PATH, f"{product.id}.jpg")
    file_path = get_image_or_default(file_path)

    with open(file_path, "rb") as f:
        product.image_name.save(f"{product.id}.jpg", File(f), save=True)

print("✅ Products updated!")


# ===============================
# گالری محصولات
# ===============================
print("🔄 Updating galleries images...")

# گرفتن لیست عکس‌های واقعی محصول
product_files = os.listdir(PRODUCT_PATH) if os.path.exists(PRODUCT_PATH) else []

for gallery in ProductGallery.objects.all():

    if product_files:
        random_file = random.choice(product_files)
        file_path = os.path.join(PRODUCT_PATH, random_file)
    else:
        file_path = DEFAULT_IMAGE

    with open(file_path, "rb") as f:
        gallery.image_name.save(f"{gallery.id}.jpg", File(f), save=True)

print("✅ Galleries updated!")
print("🎉 All images successfully assigned!")
