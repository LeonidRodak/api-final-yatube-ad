from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router = DefaultRouter()
router.register("posts", PostViewSet)
router.register("groups", GroupViewSet)
router.register("follow", FollowViewSet, basename="follow")
# Вложенный роутер для комментариев — это решает большинство 403
router.register(
    r"posts/(?P<post_id>\d+)/comments", CommentViewSet, basename="comment"
)

urlpatterns = [
    path("", include(router.urls)),
]
