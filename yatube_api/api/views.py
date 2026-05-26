# viewsets - для полноценных ViewSet'ов
# mixins - для частичных (ListModelMixin, CreateModelMixin и т.д.)
from rest_framework import viewsets, mixins
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
# Фильтр для поиска по полям (используется в FollowViewSet)
from rest_framework.filters import SearchFilter


from posts.models import Post, Group, Comment, Follow
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer,
)
from .permissions import IsAuthorOrReadOnly

# Базовый класс пагинации (limit и offset)
from rest_framework.pagination import LimitOffsetPagination


class OptionalLimitOffsetPagination(LimitOffsetPagination):
    """Пагинация только если переданы limit/offset — иначе возвращаем\
        весь список (для pytest)"""

    def paginate_queryset(self, queryset, request, view=None):
        """Переопределяем метод, который отвечает за пагинацию"""
        if (
            "limit" not in request.query_params
            and "offset" not in request.query_params
        ):
            # Если пользователь не передал limit и offset — отключаем пагинацию
            return None  # pytest будет получать просто список
        # Если параметры переданы — используем стандартную пагинацию
        return super().paginate_queryset(queryset, request, view)


class PostViewSet(viewsets.ModelViewSet):
    """Полноценный ViewSet для постов (все CRUD-операции)"""
    queryset = Post.objects.all()  # все посты из базы
    serializer_class = PostSerializer  # как сериализовать/десериализовать
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    pagination_class = OptionalLimitOffsetPagination

    def perform_create(self, serializer):
        """Выполняется перед сохранением нового поста"""
        serializer.save(author=self.request.user)  # автоматически присваиваем автора


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # отключаем пагинацию (важно для тестов)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = None   # отключаем пагинацию (важно для тестов)

    def get_queryset(self):
        """Фильтруем комментарии по post_id из URL"""
        # Безопасно достаём ID поста из URL
        post_id = self.kwargs.get("post_id")
        # Оставляем комментарии, которые отностяся к посту
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        """При создании комментария автоматически подставляем автора и пост"""
        post_id = self.kwargs.get("post_id")
        serializer.save(author=self.request.user, post_id=post_id)  # post_id потому что его передаем в сериалезаторе
 

class FollowViewSet(
    mixins.ListModelMixin, # позволяет GET /follow/ (список подписок)
    mixins.CreateModelMixin, # позволяет POST /follow/ (создать подписку)
    viewsets.GenericViewSet  # базовый класс без готовых действий
):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["following__username"]  # ищем по username того, на кого подписаны
    pagination_class = None  # отключаем пагинацию (важно для тестов)

    def get_queryset(self):
        """Возвращаем только подписки текущего пользователя"""
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании подписки автоматически подставляем текущего пользователя"""
        serializer.save(user=self.request.user)
