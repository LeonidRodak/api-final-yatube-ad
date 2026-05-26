from rest_framework import serializers
from posts.models import Post, Group, Comment, Follow
from django.contrib.auth import get_user_model

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", # вместо id пользователя выводим его username
        read_only=True
    )

    class Meta:
        model = Post
        fields = ("id", "author", "text", "pub_date", "image", "group")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    # Самый надёжный вариант для Postman-тестов
    # Вместо вложенного объекта поста выводим только его id
    post = serializers.IntegerField(source="post_id", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "text", "created", "post")
        read_only_fields = ("post",)  # поле post нельзя менять при создании комментария


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    # Выводим username пользователя, который подписывается (только для чтения)
    user = serializers.ReadOnlyField(source="user.username")
    following = serializers.SlugRelatedField(
        slug_field="username", 
        queryset=User.objects.all()  # позволяет передавать username при создании подписки
    )

    def validate(self, data):  # data - словарь из полей из fields в классе meta
        """Валидация данных перед сохранением"""
        user = self.context["request"].user  # текущий авторизованный пользователь
        following = data.get("following")  # пользователь, на которого хотят подписаться

        # Запрещаем подписку на самого себя
        if user == following:
            raise serializers.ValidationError(
                {"following": "Нельзя подписаться на самого себя."}
            )

        return data

    def create(self, validated_data):
        """Переопределяем создание, чтобы избежать дублирования подписок"""
        user = self.context["request"].user
        following = validated_data["following"]
        # get_or_create - если подписка уже есть, просто возвращаем её (не создаём дубликат)
        follow, _ = Follow.objects.get_or_create(
            user=user, following=following
        )
        return follow

    def to_representation(self, instance):
        """Определяем, как именно будет выглядеть ответ в JSON"""
        """Правильная структура ответа для Postman"""
        return {
            # instance - это объект модели Follow, который был создан или получен из базы данных
            "user": instance.user.username,
            "following": instance.following.username,
        }

    class Meta:
        model = Follow
        fields = ("user", "following")
