from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from products.models import Category, Product
from cart.models import  CartItem
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from .serializers import (
    LoginSerializer,
    UserRegistrationSerializer,
    ProductSerializer,
    ProductCreateSerializer,
    CartItemAddSerializer,
    CartItemSerializer,
    # ShoppingCartSerializer,
    # CartItemSerializer,
    # CartSerializer,
    # AddCartItemSerializer,
    # CartItemSerializer
)
from rest_framework import filters
from django.contrib.auth import get_user_model
from django.db.models import Sum, F
from django.contrib.auth import authenticate
# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin



# User Api view
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
# # Get cart
# class CartListAPIView(generics.ListAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer


# Pagination product list
class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# Products list
class ProductListCreateAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Filtering, Searching, Sort
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["title", "status", "category"]
    search_fields = ["title", "description", "status"]
    ordering_fields = ["title", "status", "category"]
    # Pagination
    pagination_class = CustomPageNumberPagination


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


#  Login api
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            password = serializer.validated_data["password"]
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                # Authentication successful
                # return Response(
                #     {"message": "Authentication successful"}, status=status.HTTP_200_OK
                # )
                # token, created = Token.objects.get_or_create(user=user)
                # return Response({'token': token.key}, status=status.HTTP_200_OK)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )
            else:
                # Authentication failed
                return Response(
                    {"message": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            # Invalid data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Register api
class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Check if user exits
            phone_number = serializer.validated_data['phone_number']
            if User.objects.filter(phone_number=phone_number).exists():
                return Response({'error': 'User with the provided username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile Details
class UserDetailsAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        data = {
            "phone_number": user.phone_number,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return Response(data)


# Create new product
class ProductCreateAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get access token api
class TokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


# class CartViewSet(CreateModelMixin,RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

# cart
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartItemView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'product__title', 'product__description', 'product__category__name']

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)


class CartItemAddView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemAddSerializer
    permission_classes = (permissions.IsAuthenticated, )


# User = get_user_model()
# User = get_user_model()

# class ShoppingCartViewSet(viewsets.ModelViewSet):
#     queryset = ShoppingCart.objects.all()
#     serializer_class = ShoppingCartSerializer

#     def create(self, request, *args, **kwargs):
#         phone_number = request.data.get('phone_number')
#         if not phone_number:
#             return Response({'error': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
#         cart, created = ShoppingCart.objects.get_or_create(phone_number=phone_number)
#         product_id = request.data.get('product_id')
#         quantity = request.data.get('quantity')
#         product = Product.objects.get(pk=product_id)
#         cart_item, created = CartItem.objects.get_or_create(
#             shopping_cart=cart,
#             product=product
#         )
#         cart_item.quantity = quantity
#         cart_item.save()
#         total_price = cart.products.aggregate(total_price=Sum(F('price') * F('cartitem__quantity')))['total_price']
#         return Response({'total_price': total_price})
# class CartView(APIView):
#     def get(self, request):
#         user = request.user
#         cart_items = CartItem.objects.filter(user=user)
#         total_price = sum(item.total_price() for item in cart_items)

#         serializer = CartItemSerializer(cart_items, many=True)
#         data = {
#             'total_price': total_price,
#             'items': serializer.data
#         }
#         return Response(data, status=status.HTTP_200_OK)

#     def post(self, request):
#         user = request.user
#         data = request.data
#         product_id = data.get('product_id')
#         quantity = data.get('quantity', 1)

#         try:
#             product = Product.objects.get(pk=product_id)
#         except Product.DoesNotExist:
#             return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

#         cart_item, created = CartItem.objects.get_or_create(user=user, product=product)
#         cart_item.quantity += int(quantity)
#         cart_item.save()
# class CartView(generics.ListAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

# class AddToCartView(APIView):
#     def post(self, request):
#         product_id = request.data.get('product_id')
#         quantity = request.data.get('quantity')

#         if not product_id or not quantity:
#             return Response({'error': 'Both product_id and quantity are required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             product = Product.objects.get(pk=product_id)
#         except Product.DoesNotExist:
#             return Response({'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)

#         cart, _ = Cart.objects.get_or_create(user=request.user)
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

#         if not created:
#             cart_item.quantity += int(quantity)
#             cart_item.save()
#         else:
#             cart_item.quantity = int(quantity)
#             cart_item.save()

#         serializer = CartSerializer(cart)
#         return Response(serializer.data)
# class CartItemViewSet(ModelViewSet):
    
#     def get_queryset(self):
#         return Cartitems.objects.filter(cart_id=self.kwargs["cart_pk"])
    
    
#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return AddCartItemSerializer
        
#         return CartItemSerializer
    
#     def get_serializer_context(self):
#         return {"cart_id": self.kwargs["cart_pk"]}