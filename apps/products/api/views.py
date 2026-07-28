from rest_framework.generics import ListAPIView, RetrieveAPIView,CreateAPIView, UpdateAPIView, DestroyAPIView
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import ProductPagination
from apps.products.services.product_service import ProductService
from apps.core.response import ApiResponse
from drf_spectacular.utils import (extend_schema,OpenApiParameter,OpenApiResponse,OpenApiExample,extend_schema_view)
# =============================================================================================
@extend_schema(
    tags=["Products"],

    summary="List active products",

    description="""
Retrieve a paginated list of active products.

Features:
- Pagination
- Search
- Ordering
- Brand filtering

Only active products are returned.
""",

    parameters=[

        OpenApiParameter(
            name="page",
            type=int,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Page number.",
        ),

        OpenApiParameter(
            name="search",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Search by product name or description.",
        ),

        OpenApiParameter(
            name="ordering",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Order by price or id. Example: price, -price",
        ),

        OpenApiParameter(
            name="brand__brand_title",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description="Filter products by brand title.",
        ),

    ],

    responses={
        200: OpenApiResponse(
            response=ProductSerializer,
            description="Products retrieved successfully.",
        ),

        400: OpenApiResponse(
            description="Invalid request parameters.",
        ),

        401: OpenApiResponse(
            description="Authentication credentials were not provided.",
        ),

        403: OpenApiResponse(
            description="Permission denied.",
        ),
    },

    examples=[
        OpenApiExample(
            name="Successful Response",
            summary="List Products",
            response_only=True,
            value={
                "success": True,
                "message": "Products retrieved successfully.",
                "data": {
                    "count": 15,
                    "next": None,
                    "previous": None,
                    "results": [
                        {
                            "id": 1,
                            "product_name": "Nike Shoes",
                            "price": "2500"
                        }
                    ]
                }
            },
        )
    ],
)
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return ApiResponse.success(
                data=self.get_paginated_response(serializer.data).data,
                message="Products retrieved successfully."
            )

        serializer = self.get_serializer(queryset, many=True)

        return ApiResponse.success(
            data=serializer.data,
            message="Products retrieved successfully."
        )
# =============================================================================================
@extend_schema(
    tags=["Products"],
    summary="Retrieve product details",
    description="""
Retrieve details of a single active product.

Returns the complete information for one product.

Only active products are returned.
""",
    responses={
        200: OpenApiResponse(
            response=ProductSerializer,
            description="Product retrieved successfully.",
            examples=[
                OpenApiExample(
                    "Product Detail",
                    value={
                        "success": True,
                        "message": "Product retrieved successfully.",
                        "data": {
                            "id": 1,
                            "product_name": "Nike Air Max",
                            "price": 250,
                            "brand": {
                                "id": 1,
                                "brand_title": "Nike"
                            },
                            "slug": "nike-air-max"
                        }
                    },
                    response_only=True,
                )
            ]
        ),
        404: OpenApiResponse(description="Product not found."),
    },
)

class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return ProductService.get_active_products()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return ApiResponse.success(
            data=serializer.data,
            message="Product retrieved successfully."
        )
# =============================================================================================
@extend_schema_view(
    post=extend_schema(
        operation_id="create_product",
    )
)

@extend_schema(
    tags=["Products"],
    summary="Create a new product",
    description="""
Creates a new product.

Permissions:
- Admin users only.

If the Brand or ProductGroup does not exist,
they will be created automatically.
""",
    request=ProductSerializer,
    responses={
        201: OpenApiResponse(
            response=ProductSerializer,
            description="Product created successfully.",
        ),
        400: OpenApiResponse(
            description="Validation Error",
        ),
        401: OpenApiResponse(
            description="Authentication required.",
        ),
        403: OpenApiResponse(
            description="Only administrators can create products.",
        ),
    },
    examples=[
        OpenApiExample(
            "Create Product Example",
            value={
                "product_name": "Nike Air Max",
                "price": 2500,
                "brand": "Nike",
                "product_group": "Shoes",
                "description": "Running shoes",
                "summery_description": "Comfortable running shoes",
                "is_active": True,
            },
            request_only=True,
        )
    ],
)
class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductService.get_all_products()

    def perform_create(self, serializer):
        serializer.save()
# =============================================================================================
@extend_schema_view(
    put=extend_schema(
        operation_id="update_product",
    ),
    patch=extend_schema(
        operation_id="partial_update_product",
    ),
)

@extend_schema(
    tags=["Products"],
    summary="Update existing product",
    description="""
Update an existing product.

Permissions:
- Admin users only.

Supports both:
- PUT (full update)
- PATCH (partial update)
""",
    request=ProductSerializer,
    responses={
        200: OpenApiResponse(
            response=ProductSerializer,
            description="Product updated successfully.",
            examples=[
                OpenApiExample(
                    "Update Product",
                    value={
                        "success": True,
                        "message": "Product updated successfully.",
                        "data": {
                            "id": 1,
                            "product_name": "Nike Air Max Updated",
                            "price": 280,
                            "brand": {
                                "id": 1,
                                "brand_title": "Nike"
                            },
                            "slug": "nike-air-max"
                        }
                    },
                    response_only=True,
                )
            ],
        ),
        400: OpenApiResponse(description="Validation Error."),
        401: OpenApiResponse(description="Authentication required."),
        403: OpenApiResponse(description="Only administrators can update products."),
        404: OpenApiResponse(description="Product not found."),
    },
)

class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductService.get_all_products()

    def perform_update(self, serializer):
        serializer.save()

# =============================================================================================
@extend_schema_view(
    delete=extend_schema(
        operation_id="delete_product",
    )
)

@extend_schema(
    tags=["Products"],
    summary="Delete product",
    description="""
Deletes an existing product.

Permissions:
- Admin users only.

This operation permanently removes the product.
""",
    responses={
        204: OpenApiResponse(
            description="Product deleted successfully."
        ),
        401: OpenApiResponse(
            description="Authentication required."
        ),
        403: OpenApiResponse(
            description="Only administrators can delete products."
        ),
        404: OpenApiResponse(
            description="Product not found."
        ),
    },
)

class ProductDeleteAPIView(DestroyAPIView):
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductService.get_all_products()

    def perform_destroy(self, instance):
        ProductService.delete_product(instance)