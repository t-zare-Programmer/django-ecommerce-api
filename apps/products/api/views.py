from rest_framework.generics import ListAPIView, RetrieveAPIView
from apps.products.models import Product
from .serializers import ProductSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class ProductUpdateAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]

class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]

