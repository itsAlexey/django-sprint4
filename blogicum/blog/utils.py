from django.db.models import Count
from django.utils import timezone


def published_posts(queryset):
    """Фильтрация постов: только опубликованные и уже доступные."""
    return (
        queryset.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True,
        )
        .annotate(comment_count=Count("comments"))
        .select_related("author", "location", "category")
        .order_by("-pub_date")
    )
