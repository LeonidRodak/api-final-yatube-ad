from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем аутентифицированным пользователям.
    Изменение и удаление - только автору объекта.
    """
    def has_object_permission(self, request, view, obj):
        # Безопасные методы (GET, HEAD, OPTIONS) - разрешены всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Проверяем, является ли текущий пользователь (request.user) автором объекта
        return obj.author == request.user
