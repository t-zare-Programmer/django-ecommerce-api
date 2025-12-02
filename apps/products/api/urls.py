from django.urls import path
from .views import (
    ProductListAPIView,
    ProductDetailAPIView,
    ProductCreateAPIView,
    ProductUpdateAPIView,
    ProductDeleteAPIView,
)

urlpatterns = [
# CRUD:
    path('products/create/', ProductCreateAPIView.as_view(), name='api_product_create'),
    path('products/<slug:slug>/update/', ProductUpdateAPIView.as_view(), name='api_product_update'),
    path('products/<slug:slug>/delete/', ProductDeleteAPIView.as_view(), name='api_product_delete'),

    path('products/', ProductListAPIView.as_view(), name='api_products'),
    path('products/<slug:slug>/', ProductDetailAPIView.as_view(), name='api_product_detail'),
]
