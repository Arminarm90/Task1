from django.urls import path, include
from .views import (
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    LoginAPIView,
    UserRegistrationAPIView,
    UserDetailsAPIView,
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    ProductCreateAPIView,
    TokenRefreshView,
    CartItemView,
    CartItemAddView,
    CartDeleteAPIView,
    # SendRequestAPIView,
    PaymentView,
    CartView,
    # CartItemDelView,

)

urlpatterns = [
    # user api
    path("users/", UserListCreateAPIView.as_view(), name="user-list-create"),
    path(
        "users/<int:pk>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-detail",
    ),
    path("login/", LoginAPIView.as_view(), name="api-login"),
    path("register/", UserRegistrationAPIView.as_view(), name="register-login"),
    path("profile/", UserDetailsAPIView.as_view(), name="user-profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # product api
    path("products/", ProductListCreateAPIView.as_view(), name="products-list-create"),
    path(
        "products/<int:pk>/",
        ProductRetrieveUpdateDestroyAPIView.as_view(),
        name="products-detail",
    ),
    path("products/create/", ProductCreateAPIView.as_view(), name="create_product"),
    # cart api
    path('cart/', CartView.as_view(), name='cart'),
    path("cart-datail/", CartItemView.as_view(), name="cart-detail"),
    path("cart/add/", CartItemAddView.as_view(), name='cart-add'),
    path('cart/delete/<int:cart_id>/', CartDeleteAPIView.as_view(), name='card-delete'),

    # Zarinpal 
    # path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/', PaymentView.as_view(), name='payment'),


]
