from django.contrib import admin

from .models import Category, Location, Post, Comment


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "created_at")
    list_editable = ("is_published",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",
                    "description",
                    "slug",
                    "is_published",
                    "created_at")
    list_editable = ("is_published",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title",
                    "author",
                    "category",
                    "location",
                    "is_published",
                    "pub_date",
                    "comment_count")
    list_editable = ("is_published",)
    list_filter = ("category", "location")

    @admin.display(description="Комментариев")
    def comment_count(self, post):
        return post.comments.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_at")
    list_filter = ("created_at",)
