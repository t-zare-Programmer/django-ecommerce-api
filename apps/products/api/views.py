from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView, UpdateAPIView, DestroyAPIView
from apps.products.models import Product
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ProductPagination
from apps.products.services.product_service import ProductService

# =============================================================================================
class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    pagination_class = ProductPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['brand__brand_title']
    search_fields = ['product_name', 'description']
    ordering_fields = ['price', 'id']

    def get_queryset(self):
        return ProductService.get_active_products()
# =============================================================================================
class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return ProductService.get_active_products()
# =============================================================================================
class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductService.get_all_products()

    def perform_create(self, serializer):
        serializer.save()
# =============================================================================================
class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductService.get_all_products()

    def perform_update(self, serializer):
        serializer.save()

# =============================================================================================
class ProductDeleteAPIView(DestroyAPIView):
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductService.get_all_products()

    def perform_destroy(self, instance):
        ProductService.delete_product(instance)