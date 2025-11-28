from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.products.models import Product
from .serializers import ProductSerializer


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
