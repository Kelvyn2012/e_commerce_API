from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models import Count, Sum, Q  # Add Q here
from .models import Product, Category, Order
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
)
from .permissions import IsOwnerOrReadOnly
from .filters import ProductFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:  # public routes
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category", "owner").all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name", "category__name"]  # partial matches
    ordering_fields = ["price", "created_at", "name"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Ensure owner cannot be changed during update."""
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"])
    def by_category(self, request):
        """Get products by category slug."""
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

    @action(detail=False, methods=["get"])
    def low_stock(self, request):
        """Get products with low stock (less than 10 items)."""
        threshold = int(request.query_params.get("threshold", 10))
        qs = self.get_queryset().filter(
            stock_quantity__lte=threshold, stock_quantity__gt=0
        )

        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)

        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)

    @action(detail=False, methods=["get"])
    def out_of_stock(self, request):
        """Get products that are out of stock."""
        qs = self.get_queryset().filter(stock_quantity=0)

        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)

        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)

    @action(detail=True, methods=["post"])
    def check_availability(self, request, pk=None):
        """Check if requested quantity is available."""
        product = self.get_object()
        quantity = request.data.get("quantity", 1)

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response(
                {"error": "Quantity must be a valid number"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if quantity <= 0:
            return Response(
                {"error": "Quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        available = product.stock_quantity >= quantity

        return Response(
            {
                "product": product.name,
                "requested_quantity": quantity,
                "available_stock": product.stock_quantity,
                "is_available": available,
                "message": f"{'Available' if available else 'Insufficient stock'}",
            }
        )


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders with atomic stock validation.
    """

    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status", "created_at"]
    ordering_fields = ["created_at", "total_amount"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """
        Users can only see their own orders unless they're staff.
        Staff can see all orders.
        """
        if self.request.user.is_staff:
            return (
                Order.objects.select_related().prefetch_related("items__product").all()
            )

        # For regular users, show orders they created
        return (
            Order.objects.filter(customer_email=self.request.user.email)
            .select_related()
            .prefetch_related("items__product")
        )

    def create(self, request, *args, **kwargs):
        """
        Create order with stock validation.
        The serializer handles transactions automatically.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            order = serializer.save()

            headers = self.get_success_headers(serializer.data)
            return Response(
                {"order": serializer.data, "message": "Order created successfully"},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )

        except Exception as e:
            # Check if it's a validation error with stock info
            error_message = str(e)
            if "stock" in error_message.lower() or "available" in error_message.lower():
                return Response(
                    {
                        "error": "Order creation failed due to stock availability",
                        "details": error_message,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {"error": "Order creation failed", "details": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def cancel(self, request, pk=None):
        """
        Cancel an order and restore stock quantities.
        Only pending or processing orders can be cancelled.
        """
        order = self.get_object()

        # Check if user owns this order or is staff
        if not request.user.is_staff and order.customer_email != request.user.email:
            return Response(
                {"error": "You do not have permission to cancel this order"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if order.status == "cancelled":
            return Response(
                {"error": "Order is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.status == "completed":
            return Response(
                {"error": "Cannot cancel completed orders"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Restore stock for each item
        for item in order.items.all():
            product = Product.objects.select_for_update().get(pk=item.product.pk)
            product.stock_quantity += item.quantity
            product.save(update_fields=["stock_quantity"])

        # Update order status
        order.status = "cancelled"
        order.save(update_fields=["status"])

        serializer = self.get_serializer(order)
        return Response(
            {
                "order": serializer.data,
                "message": "Order cancelled successfully and stock restored",
            }
        )

    @action(detail=True, methods=["post"])
    def mark_completed(self, request, pk=None):
        """
        Mark order as completed (staff only).
        """
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff can mark orders as completed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        order = self.get_object()

        if order.status == "completed":
            return Response(
                {"error": "Order is already completed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.status == "cancelled":
            return Response(
                {"error": "Cannot complete a cancelled order"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = "completed"
        order.save(update_fields=["status"])

        serializer = self.get_serializer(order)
        return Response(
            {"order": serializer.data, "message": "Order marked as completed"}
        )

    @action(detail=True, methods=["post"])
    def mark_processing(self, request, pk=None):
        """
        Mark order as processing (staff only).
        """
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff can mark orders as processing"},
                status=status.HTTP_403_FORBIDDEN,
            )

        order = self.get_object()

        if order.status != "pending":
            return Response(
                {"error": "Only pending orders can be marked as processing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = "processing"
        order.save(update_fields=["status"])

        serializer = self.get_serializer(order)
        return Response(
            {"order": serializer.data, "message": "Order marked as processing"}
        )

    @action(detail=False, methods=["get"])
    def my_orders(self, request):
        """
        Get current user's orders.
        """
        orders = (
            Order.objects.filter(customer_email=request.user.email)
            .select_related()
            .prefetch_related("items__product")
        )

        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """
        Get order statistics (staff only).
        """
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff can view statistics"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Fixed: Use Q from django.db.models, not models.Q
        stats = Order.objects.aggregate(
            total_orders=Count("id"),
            total_revenue=Sum("total_amount"),
            pending_orders=Count("id", filter=Q(status="pending")),
            processing_orders=Count("id", filter=Q(status="processing")),
            completed_orders=Count("id", filter=Q(status="completed")),
            cancelled_orders=Count("id", filter=Q(status="cancelled")),
        )

        return Response(stats)
