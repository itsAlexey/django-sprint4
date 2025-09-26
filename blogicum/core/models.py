from django.db import models


class PublicationTimestamps(models.Model):
    """Абстрактная модель для публикаций с временными метками."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class BaseTitle(models.Model):
    """Базовая модель с заголовком."""

    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок',
    )

    class Meta:
        abstract = True
