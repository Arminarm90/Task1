from django.urls import path, include
from .views import (
    UserListCreateAPIView,
    # CartListAPIView,
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
    # ProductViewSet,
    # ShoppingCartViewSet,
    # CartView,
    # CartView,
    # AddToCartView
)
from rest_framework.routers import DefaultRouter

# from rest_framework.routers import DefaultRouter
# from rest_framework_nested import routers
# from . import views

# router = routers.DefaultRouter()

# router.register("carts", views.CartViewSet)


# cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
# cart_router.register("items", views.CartItemViewSet, basename="cart-items")

# router = DefaultRouter()
# router.register(r"products", ProductViewSet)
# router.register(r"shopping_carts", ShoppingCartViewSet)

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
    path("cart/", CartItemView.as_view(), name="cart"),
    path("cart/add/", CartItemAddView.as_view()),
    # path("", include(router.urls)),
    # path('cart/', CartView.as_view(),name="cart"),
    # path('cart/add/', AddToCartView.as_view(),name="cart-add"),
    # path("", include(router.urls)),
    # path("", include(cart_router.urls))
    # path("cart/", CartListAPIView.as_view(), name="cart"),
    # path("cart-items/", CartItemViewSet.as_view(), name="cart-items"),
    # path("cart/", CartItemViewSet.as_view(), name="cart"),
]
