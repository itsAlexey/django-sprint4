from django.contrib import admin

from .models import Category, Location, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Управление категориями в админке."""

    list_display = ("title", "slug", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("title", "slug")
    list_filter = ("is_published",)
    ordering = ("-created_at",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Управление локациями (местами)."""

    list_display = ("name", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("name",)
    list_filter = ("is_published",)
    ordering = ("name",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админка постов."""

    list_display = (
        "title",
        "author",
        "pub_date",
        "category",
        "location",
        "is_published",
        "comment_count",
    )
    list_editable = ("is_published",)
    list_filter = ("category", "location", "is_published")
    search_fields = ("title", "author__username")
    ordering = ("-pub_date",)
    list_select_related = ("author", "category", "location")

    @admin.display(description="Комментарии")
    def comment_count(self, obj):
        """Подсчёт числа комментариев для поста."""
        return obj.comments.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка комментариев."""

    list_display = ("author", "post", "created_at", "is_published")
    list_editable = ("is_published",)
    search_fields = ("text", "author__username")
    list_filter = ("created_at", "is_published")
    ordering = ("-created_at",)
