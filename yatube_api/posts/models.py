from django.db import models
from django.contrib.auth import get_user_model  # возвращает текущую модель пользователя

User = get_user_model()


class Post(models.Model):
    """Модель публикации (поста) в социальной сети"""
    author = models.ForeignKey(
        User, 
        # Если пользователь удаляется - удаляются все его посты
        on_delete=models.CASCADE, 
        # Позволяет обращаться к постам пользователя через user.posts.all()
        related_name="posts"
    )
    text = models.TextField()
    # Человекочитаемое название поля в админке
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    image = models.ImageField(
        "Картинка", upload_to="posts/", blank=True, null=True
    )
    group = models.ForeignKey(
        "Group",  # строка, потому что модель Group объявлена ниже
        on_delete=models.SET_NULL,  # если группа удаляется - поле становится NULL (пост остаётся)
        related_name="posts",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["-pub_date"]  # сортировка новые посты сверху

    def __str__(self):
        return self.text[:15]  # в админке будет показываться название


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)  # человекопонятный URL
    description = models.TextField()

    def __str__(self):
        return self.title  # в админке и shell будет показываться название


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created = models.DateTimeField("Дата комментария", auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.text[:15]  # краткое отображение комментария


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        # Список ограничений
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"],   # уникальный индекс на пару полей
                name="unique_follow"  # название ограничения
            )
        ]

    def __str__(self):
        return f"{self.user} подписан на {self.following}"
