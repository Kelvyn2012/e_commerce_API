from rest_framework import serializers
from .models import Product, Category, Order, OrderItem
from django.db import transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {"slug": {"read_only": True}}


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, source="category"
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "category_id",
            "stock_quantity",
            "image_url",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "subtotal",
        ]
        read_only_fields = ["id", "subtotal"]

    def validate(self, data):
        product = data.get("product")
        quantity = data.get("quantity")

        if quantity > product.stock_quantity:
            raise serializers.ValidationError(
                {
                    "quantity": f"Only {product.stock_quantity} units available for {product.name}."
                }
            )

        if quantity <= 0:
            raise serializers.ValidationError(
                {"quantity": "Quantity must be greater than 0."}
            )

        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    customer_email = serializers.EmailField()

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_email",
            "items",
            "total_amount",
            "status",
            "created_at",
        ]
        read_only_fields = ["id", "total_amount", "created_at"]

    def validate_customer_email(self, value):
        if not value or "@" not in value:
            raise serializers.ValidationError("Please provide a valid email address.")
        return value.lower()

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        """
        Create order with atomic transaction.
        If any step fails, everything rolls back automatically.
        """
        items_data = validated_data.pop("items")

        # Create the order
        order = Order.objects.create(**validated_data)

        total_amount = 0

        try:
            for item_data in items_data:
                product = item_data["product"]
                quantity = item_data["quantity"]

                # Use select_for_update to lock the product row
                # This prevents race conditions with concurrent orders
                product = Product.objects.select_for_update().get(pk=product.pk)

                # Re-check stock after locking (stock might have changed)
                if quantity > product.stock_quantity:
                    raise serializers.ValidationError(
                        {
                            "items": f"Insufficient stock for {product.name}. Only {product.stock_quantity} available."
                        }
                    )

                # Create order item
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price,  # Save price at time of order
                )

                # Reduce stock
                product.stock_quantity -= quantity
                product.save(update_fields=["stock_quantity"])

                # Calculate total
                total_amount += order_item.subtotal

            # Update order total
            order.total_amount = total_amount
            order.save(update_fields=["total_amount"])

            return order

        except Exception as e:
            # Transaction will automatically rollback
            # Re-raise the exception to let DRF handle it
            raise

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Handle order updates with transaction protection.
        """
        items_data = validated_data.pop("items", None)

        # Update basic order fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            # This is complex - you might want to prevent updates
            # or handle stock restoration for cancelled items
            raise serializers.ValidationError(
                "Order items cannot be modified after creation. Please create a new order."
            )

        return instance
