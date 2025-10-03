from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from core.models import PublicationTimestamps, BaseTitle

User = get_user_model()

MAX_STR_LENGTH = 30
COMMENT_PREVIEW = 20


class Location(PublicationTimestamps):
    """Местоположения постов."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название места",
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self) -> str:
        return self.name[:MAX_STR_LENGTH]


class Category(PublicationTimestamps, BaseTitle):
    """Категории постов."""

    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.title[:MAX_STR_LENGTH]

    def get_absolute_url(self) -> str:
        return reverse("blog:category_posts",
                       kwargs={"category_slug": self.slug})


class Post(PublicationTimestamps, BaseTitle):
    """Публикации блога."""

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
        null=True,  # сохраняем поведение из исходного кода
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name="Категория",
    )
    image = models.ImageField(
        verbose_name="Изображение",
        upload_to="post_images",
        blank=True,
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)
        default_related_name = "posts"

    def __str__(self) -> str:
        return self.title[:MAX_STR_LENGTH]

    def get_absolute_url(self) -> str:
        return reverse("blog:post_detail", kwargs={"pk": self.pk})


class Comment(PublicationTimestamps):
    """Комментарии к постам."""

    text = models.TextField(verbose_name="Комментарий")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Публикация",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)
        default_related_name = "comments"

    def __str__(self) -> str:
        return self.text[:COMMENT_PREVIEW]
