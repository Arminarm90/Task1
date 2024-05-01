from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate
from products.models import Category, Product
from cart.models import  CartItem
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
        
# Cart
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# Cart
class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    # total_price = sum(item.product.price * item.quantity for item in product)

    class Meta:
        model = CartItem
        fields = ('id', 'quantity', 'product')


class CartItemAddSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField(source="product.title", read_only=True)


    class Meta:
        model = CartItem
        fields = ['quantity', 'product_id']
        extra_kwargs = {
            'quantity': {'required': True},
            'product_id': {'required': True},
            # 'total_price': {'required': True},
        }
        
    def create(self, validated_data):
        user = User.objects.get(id=self.context['request'].user.id)
        product = get_object_or_404(Product, id=validated_data['product_id'])
        cart_item = CartItem.objects.create(
            product=product,
            user=user,
            quantity=validated_data['quantity']
            )
        cart_item.save()
        product.save()
        return cart_item
