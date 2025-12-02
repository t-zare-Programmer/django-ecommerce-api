from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.main.urls', namespace='main')),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('discounts/', include('apps.discounts.urls', namespace='discounts')),
    path('payments/', include('apps.payments.urls', namespace='payments')),
    path('warehouses/', include('apps.warehouses.urls', namespace='warehouses')),
    path('csf/', include('apps.comment_scoring_favorites.urls', namespace='csf')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include('apps.products.api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
