from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from products.models import Category, Product
from cart.models import CartItem
from .serializers import UserSerializer
from .serializers import (
    LoginSerializer,
    UserRegistrationSerializer,
    ProductSerializer,
    ProductCreateSerializer,
    CartItemAddSerializer,
    CartItemSerializer,
    SendRequestSerializer,
    VerifySerializer,
    CombinedCartSerializer,
    AggregatedCartSerializer,
)
from rest_framework import filters
from django.contrib.auth import authenticate

# from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.conf import settings
import requests
import json
from zeep import Client
from core.settings import MERCHANT


# User Api view
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
            phone_number = serializer.validated_data["phone_number"]
            if User.objects.filter(phone_number=phone_number).exists():
                return Response(
                    {
                        "error": "User with the provided username or email already exists"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    # permission_classes = (permissions.IsAuthenticated, )
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "product__title",
        "product__description",
        "product__category__name",
    ]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)


class CartItemAddView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemAddSerializer
    # permission_classes = (permissions.IsAuthenticated, )

class AggregatedCartAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        total_price = sum(item.total_price for item in cart_items)

        serializer = AggregatedCartSerializer({'cart_items': cart_items, 'total_price': total_price})
        return Response(serializer.data)
    

class CartDeleteAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, cart_id, format=None):
        user = request.user
        cart = get_object_or_404(CartItem, id=cart_id)
        if cart.user != user:
            return Response(
                {"error": "You are not authorized to delete this cart."},
                status=status.HTTP_403_FORBIDDEN,
            )
        cart.delete()
        return Response(
            {"message": "Cart deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


# Zarinpall
# ? sandbox merchant
if settings.SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = (
    f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
)
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = ""  # Required
phone = "YOUR_PHONE_NUMBER"  # Optional
# Important: need to edit for realy server.
CallbackURL = "http://127.0.0.1:8000/api/"


# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 1000  # Rial / Required
description = "Description"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8080/verify/'


class PaymentView(APIView):

    def post(self, request):
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Description": description,
            "Phone": phone,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    return Response({
                        'status': True,
                        'payment_url': ZP_API_STARTPAY + str(response_data['Authority']),
                        'authority': response_data['Authority']
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'status': False, 'code': str(response_data['Status'])},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.Timeout:
            return Response({'status': False, 'code': 'timeout'}, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.ConnectionError:
            return Response({'status': False, 'code': 'connection error'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        authority = request.query_params.get('authority')
        if authority:
            data = {
                "MerchantID": settings.MERCHANT,
                "Amount": amount,
                "Authority": authority,
            }
            data = json.dumps(data)
            headers = {'content-type': 'application/json', 'content-length': str(len(data))}
            response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    return Response({'status': True, 'RefID': response_data['RefID']}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': False, 'code': str(response_data['Status'])},
                                    status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': False, 'code': 'authority not provided'}, status=status.HTTP_400_BAD_REQUEST)
