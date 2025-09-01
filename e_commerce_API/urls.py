from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views import ProductViewSet, CategoryViewSet
from users.views import UserViewSet, RegisterView, login_view
from rest_framework.authtoken.views import obtain_auth_token
from django.http import JsonResponse

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")


def home(request):
    return JsonResponse({"message": "Welcome to the E-commerce API 🚀"})


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/token/", obtain_auth_token, name="api_token_auth"),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", login_view, name="login"),
]
