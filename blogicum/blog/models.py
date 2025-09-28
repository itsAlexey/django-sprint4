from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from core.models import PublicationTimestamps, BaseTitle

User = get_user_model()
TEXT_LENGTH = 256
MAX_STR_LENGTH = 15


class Category(PublicationTimestamps, BaseTitle):
    """Категории постов."""

    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:MAX_STR_LENGTH]


class Location(PublicationTimestamps):
    """Местоположения постов."""

    name = models.CharField(
        max_length=TEXT_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:MAX_STR_LENGTH]


class Post(PublicationTimestamps, BaseTitle):
    """Посты."""

    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )
    image = models.ImageField(
        upload_to="posts_images/",
        blank=True,
        null=True,
        verbose_name="Картинка"
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:MAX_STR_LENGTH]

    @property
    def is_visible(self):
        """Пост виден всем: опубликован + не в будущем."""
        return self.is_published and self.pub_date <= timezone.now()


class Comment(PublicationTimestamps):
    """Комментарии к постам."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Публикация",
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор комментария",
        related_name="comments",
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:MAX_STR_LENGTH]