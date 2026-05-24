from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView, UpdateAPIView, DestroyAPIView
from apps.products.models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['brand__brand_title']
    search_fields = ['product_name', 'description']
    ordering_fields = ['price', 'id']


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class ProductCreateAPIView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductUpdateAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

class ProductDeleteAPIView(DestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

