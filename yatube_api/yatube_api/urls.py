from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
# Импортируем готовые View для работы с JWT-токенами
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # для получения access и refresh токенов
    TokenRefreshView,  # для обновления access-токена
    TokenVerifyView,  # для проверки валидности токена
)
# TemplateView — простой класс для отображения HTML-шаблона (используется для Redoc)
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    # JWT-эндпоинты - ОБЯЗАТЕЛЬНО ПЕРЕД include('api.urls')
    
    # Эндпоинт для входа: POST /api/v1/jwt/create/
    # Принимает username + password и возвращает access + refresh токены
    path(
        "api/v1/jwt/create/",
        TokenObtainPairView.as_view(
            permission_classes=[AllowAny],  # любой пользователь может получить токен
            authentication_classes=[],  # не требуем аутентификацию для получения токена
        ),
        name="token_obtain_pair",
    ),
    # Эндпоинт для обновления токена: POST /api/v1/jwt/refresh/
    # Принимает refresh-токен и возвращает новый access-токен
    path(
        "api/v1/jwt/refresh/",
        TokenRefreshView.as_view(
            permission_classes=[AllowAny],
            authentication_classes=[],
        ),
        name="token_refresh",
    ),
    # Эндпоинт для проверки токена: POST /api/v1/jwt/verify/
    # Проверяет, действителен ли access-токен
    path(
        "api/v1/jwt/verify/",
        TokenVerifyView.as_view(
            permission_classes=[AllowAny],
            authentication_classes=[],
        ),
        name="token_verify",
    ),
    # Подключаем все маршруты из файла api/urls.py
    path("api/v1/", include("api.urls")),
    # Отображает красивую документацию Redoc по адресу /redoc/
    path(
        "redoc/",
        TemplateView.as_view(template_name="redoc.html"),
        name="redoc",
    ),
]
