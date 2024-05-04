from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate
from products.models import Category, Product
from cart.models import CartItem
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}


# Products serializer
class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "image",
            "description",
            "status",
            "category",
            "category_name",
        ]


# Login serializer
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()


# Register serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ("phone_number", "password", "email", "first_name", "last_name")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


#  Product create
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("title", "image", "description", "status", "category")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


# Cart
class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    # total_price = sum(item.product.price * item.quantity for item in product)

    class Meta:
        model = CartItem
        fields = ("id", "quantity", "total_price", "product")


class AggregatedCartSerializer(serializers.Serializer):
    cart_items = CartItemSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartItemAddSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["product_id", "quantity"]
        extra_kwargs = {
            "product_id": {"required": True},
            "quantity": {"required": True},
        }

    def create(self, validated_data):
        user = User.objects.get(id=self.context["request"].user.id)
        product = get_object_or_404(Product, id=validated_data["product_id"])
        cart_item = CartItem.objects.create(
            product=product,
            user=user,
            quantity=validated_data["quantity"],
        )
        cart_item.save()
        product.save()
        return cart_item

    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_title = (
            Product.objects.filter(id=instance.product_id)
            .values_list("title", flat=True)
            .first()
        )
        data["product_title"] = product_title
        instance.save()
        data["total_price"] = instance.total_price
        return data


class CombinedCartSerializer(serializers.Serializer):
    cart_items = serializers.SerializerMethodField()
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    def get_cart_items(self, obj):
        # obj here is the user instance
        carts = (
            obj.carts.all()
        )  # assuming you have a related name for the carts in the user model
        cart_items = CartItem.objects.filter(cart__in=carts)
        return CartItemSerializer(cart_items, many=True).data


# Zarinpall
class SendRequestSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "phone_number",
            "total_price",
        ]


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["price", "user"]
