from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate
from products.models import Category, Product
from cart.models import  CartItem
from django.shortcuts import get_object_or_404


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    # def create(self, validated_data):
    #     user = User.objects.create_user(**validated_data)
    #     return user


# Cart serializer
# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = ["product", "quantity", "status", "user", "date_added"]


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


class CartItemSerializer(serializers.ModelSerializer):
    """
    serializer for cartitem that serialize all fields in 'CartItem' class
    model and add 'product' as relation

    """

    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'quantity', 'product')


class CartItemAddSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ('quantity', 'product_id')
        extra_kwargs = {
            'quantity': {'required': True},
            'product_id': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.get(id=self.context['request'].user.id)
        product = get_object_or_404(Product, id=validated_data['product_id'])
        if product.quantity == 0 or product.is_available is False:
            raise serializers.ValidationsError(
                {'not available': 'the product is not available.'})

        cart_item = CartItem.objects.create(
            product=product,
            user=user,
            quantity=validated_data['quantity']
            )
        cart_item.save()
        cart_item.add_amount()
        product.quantity = product.quantity - cart_item.quantity
        product.save()
        return cart_item
# class CartItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = '__all__'

# class ShoppingCartSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = ShoppingCart
#         fields = '__all__'


# class CartItemSerializer(serializers.ModelSerializer):
#     total_price = serializers.SerializerMethodField()

#     def get_total_price(self, obj):
#         return obj.total_price()

#     class Meta:
#         model = CartItem
#         fields = ['id', 'product', 'quantity', 'total_price']
        
        
# class CartItemSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()

#     class Meta:
#         model = CartItem
#         fields = ['product_id', 'quantity']

# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'items']
 
        
# class SimpleProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ["id","title", "price"]
        
        
        

# class CartItemSerializer(serializers.ModelSerializer):
#     product = SimpleProductSerializer(many=False)
#     sub_total = serializers.SerializerMethodField( method_name="total")
#     class Meta:
#         model= Cartitems
#         fields = ["id", "cart", "product", "quantity", "sub_total"]
        
    
#     def total(self, cartitem:Cartitems):
#         return cartitem.quantity * cartitem.product.price
    

# class AddCartItemSerializer(serializers.ModelSerializer):
    
#     def validate_product_id(self, value):
#         if not Product.objects.filter(pk=value).exists():
#             raise serializers.ValidationError("There is no product associated with the given ID")
        
#         return value
    
#     def save(self, **kwargs):
#         cart_id = self.context["cart_id"]
#         product_id = self.validated_data["product_id"] 
#         quantity = self.validated_data["quantity"] 
        
#         try:
#             cartitem = Cartitems.objects.get(product_id=product_id, cart_id=cart_id)
#             cartitem.quantity += quantity
#             cartitem.save()
            
#             self.instance = cartitem
            
        
#         except:
            
#             self.instance = Cartitems.objects.create(cart_id=cart_id, **self.validated_data)
            
#         return self.instance
         

#     class Meta:
#         model = Cartitems
#         fields = ["id", "product_id", "quantity"]


# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)
#     grand_total = serializers.SerializerMethodField(method_name='main_total')
    
#     class Meta:
#         model = Cart
#         fields = ["id", "items", "grand_total"]
        
    
    
#     def main_total(self, cart: Cart):
#         items = cart.items.all()
#         total = sum([item.quantity * item.product.price for item in items])
#         return total



