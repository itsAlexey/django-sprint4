from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import PublicationTimestamps, BaseTitle

User = get_user_model()

TEXT_LENGTH = 256
MAX_STR_LENGTH = 15


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


class Post(PublicationTimestamps, BaseTitle):
    """Посты."""

    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text="Если дата в будущем — публикация будет отложенной."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Категория",
    )
    image = models.ImageField(
        upload_to="posts_images/",
        blank=True,
        null=True,
        verbose_name="Картинка",
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.title[:MAX_STR_LENGTH]

    @property
    def is_visible(self):
        return self.is_published and self.pub_date <= timezone.now()


class Comment(PublicationTimestamps):
    """Комментарии."""

    text = models.TextField(verbose_name="Текст комментария")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Публикация",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"{self.author}: {self.text[:MAX_STR_LENGTH]}"