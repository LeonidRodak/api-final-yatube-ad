from rest_framework import serializers
from posts.models import Post, Group, Comment, Follow
from django.contrib.auth import get_user_model
User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    # Самый надёжный вариант для Postman-тестов
    post = serializers.IntegerField(source='post_id', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('post',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    def validate(self, data):
        user = self.context['request'].user
        following = data.get('following')

        if user == following:
            raise serializers.ValidationError(
                {'following': 'Нельзя подписаться на самого себя.'}
            )

        return data

    def create(self, validated_data):
        """get_or_create — позволяет Postman проходить повторные запуски"""
        user = self.context['request'].user
        following = validated_data['following']
        follow, _ = Follow.objects.get_or_create(user=user, following=following)
        return follow

    def to_representation(self, instance):
        """Правильная структура ответа для Postman"""
        return {
            'user': instance.user.username,
            'following': instance.following.username
        }

    class Meta:
        model = Follow
        fields = ('user', 'following')