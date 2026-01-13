from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views import ProductViewSet, CategoryViewSet, OrderViewSet
from users.views import UserViewSet, RegisterView, LoginView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token
from django.http import JsonResponse

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")
router.register(r"orders", OrderViewSet, basename="order")


def home(request):
    return JsonResponse(
        {
            "message": "Welcome to the E-commerce API 🚀",
            "endpoints": {
                "auth": {
                    "register": "/api/auth/register/",
                    "login": "/api/auth/login/",
                    "logout": "/api/auth/logout/",
                    "token": "/api/auth/token/",
                },
                "resources": {
                    "users": "/api/users/",
                    "categories": "/api/categories/",
                    "products": "/api/products/",
                    "orders": "/api/orders/",
                },
                "user_endpoints": {
                    "me": "/api/users/me/",
                    "change_password": "/api/users/change_password/",
                },
                "product_endpoints": {
                    "by_category": "/api/products/by_category/?slug=<category-slug>",
                    "low_stock": "/api/products/low_stock/",
                    "out_of_stock": "/api/products/out_of_stock/",
                    "check_availability": "/api/products/<id>/check_availability/",
                },
                "order_endpoints": {
                    "my_orders": "/api/orders/my_orders/",
                    "cancel": "/api/orders/<id>/cancel/",
                    "mark_completed": "/api/orders/<id>/mark_completed/",
                    "mark_processing": "/api/orders/<id>/mark_processing/",
                    "statistics": "/api/orders/statistics/",
                },
            },
        }
    )


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/token/", obtain_auth_token, name="api_token_auth"),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", LoginView.as_view(), name="login"),
    path("api/auth/logout/", LogoutView.as_view(), name="logout"),  # Added LogoutView
]
