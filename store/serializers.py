from decimal import Decimal
from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import NotFound
from .signals import order_created
from .models import (
    Cart,
    CartItem,
    Customer,
    OrderItem,
    Product,
    Collection,
    ProductImage,
    Reviews,
    Order,
)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)


class ProductImageSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return ProductImage.objects.create(
            product_id=self.context["product_id"], **validated_data
        )

    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "slug",
            "inventory",
            "unit_price",
            "price_with_tax",
            "collection",
            "images",
        ]

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "unit_price",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ["id", "name", "description", "date"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        review = Reviews.objects.create(product_id=product_id, **validated_data)
        return review


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])  # type: ignore


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    def validate_product_id(self, value):
        if value < 1:
            raise NotFound("product with given id not found!")
        return value

    def save(self, **kwargs):
        product_id = self.validated_data["product_id"]  # type: ignore
        quantity = self.validated_data["quantity"]  # type: ignore
        cart_id = self.context["cart_id"]
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **self.validated_data)  # type: ignore
            self.instance = cart_item
        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ["id", "user_id", "phone", "birth_date", "membership"]


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "unit_price", "quantity"]


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["payment_status"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "customer", "placed_at", "payment_status", "items"]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("No cart with given id exist")
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError("The cart is empty")
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]  # type: ignore
            customer = Customer.objects.only("id").get(user_id=self.context["user_id"])
            order = Order.objects.create(customer_id=customer.id)  # type: ignore
            cart_items = CartItem.objects.select_related("product").filter(cart_id=self.validated_data["cart_id"])  # type: ignore
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.unit_price,
                )
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()
            order_created.send_robust(self.__class__, order=Order)
            return order
