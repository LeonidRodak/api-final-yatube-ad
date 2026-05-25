from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT-эндпоинты — ОБЯЗАТЕЛЬНО ПЕРЕД include('api.urls')
    path(
        'api/v1/jwt/create/',
        TokenObtainPairView.as_view(
            permission_classes=[AllowAny],
            authentication_classes=[],
        ),
        name='token_obtain_pair',
    ),
    path(
        'api/v1/jwt/refresh/',
        TokenRefreshView.as_view(
            permission_classes=[AllowAny],
            authentication_classes=[],
        ),
        name='token_refresh',
    ),
    path(
        'api/v1/jwt/verify/',
        TokenVerifyView.as_view(
            permission_classes=[AllowAny],
            authentication_classes=[],
        ),
        name='token_verify',
    ),

    path('api/v1/', include('api.urls')),

    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]