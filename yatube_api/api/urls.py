from django.urls import path, include
# DefaultRouter - автоматический роутер DRF, который сам генерирует URL
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

# Создаём экземпляр роутера (будет автоматически генерировать URL и маршруты для ViewSet)
router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("groups", GroupViewSet)
# basename обязателен, когда мы используем не полный ModelViewSet, а миксины (ListModelMixin + CreateModelMixin)
router.register("follow", FollowViewSet, basename="follow")
# Вложенный роутер для комментариев — это решает большинство 403
router.register(
    # r"" чтобы экранировать слеши.
    # (?P<post_id>\d+) - регулярное выражение:
    #     - post_id - имя параметра
    #     - \d+ - одна или больше цифр
    # basename="comment" - обязательно для вложенных ViewSet'ов (нужно для reverse URL)
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comment"
)

urlpatterns = [
    # Подключаем все созданные роутером URL
    path("", include(router.urls)),
]
