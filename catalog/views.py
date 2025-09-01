from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly
from .filters import ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:  # public routes
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]  #


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category", "owner").all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = ProductFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "category__name"]  # partial matches
    ordering_fields = ["price", "created_at", "name"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        slug = request.query_params.get("slug")
        qs = (
            self.get_queryset().filter(category__slug=slug)
            if slug
            else self.get_queryset()
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)
