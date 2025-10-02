from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import PublicationTimestamps, BaseTitle

User = get_user_model()
TEXT_LENGTH = 256
MAX_STR_LENGTH = 15


class Location(PublicationTimestamps):
    """Местоположения постов."""

    name = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name="Название места"
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name[:MAX_STR_LENGTH]


class Category(PublicationTimestamps, BaseTitle):
    """Категории постов."""

    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        verbose_name="Идентификатор",
        unique=True,
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title[:MAX_STR_LENGTH]

    def get_absolute_url(self):
        return reverse("blog:category_posts",
                       kwargs={"category_slug": self.slug})


class Post(PublicationTimestamps, BaseTitle):
    """Посты."""

    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name="posts",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
        related_name="posts",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="posts",
    )
    image = models.ImageField(
        upload_to="img/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)
        default_related_name = "posts"

    def __str__(self):
        return self.title[:MAX_STR_LENGTH]

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"post_id": self.pk})


class Comment(models.Model):
    """Комментарии к публикациям."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="comments",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Публикация",
        related_name="comments",
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(
        verbose_name="Дата",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)

    def __str__(self):
        return self.text[:MAX_STR_LENGTH]
