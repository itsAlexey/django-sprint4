from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse

from .models import Comment, Post

PAGE_SIZE = 10


class CustomListMixin:
    """
    Общий queryset для списков постов:
    связи, счётчик комментариев, сортировка.
    """

    model = Post
    paginate_by = PAGE_SIZE

    def get_queryset(self):
        return (
            Post.objects.select_related("category", "location", "author")
            .annotate(comment_count=Count("comments"))
            .order_by("-pub_date")
        )


class PostChangeMixin:
    """Проверка авторства при изменении/удалении поста."""

    model = Post
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect("blog:post_detail", pk=self.kwargs.get("post_id"))
        return super().dispatch(request, *args, **kwargs)


class CommentChangeMixin:
    """Проверка авторства при изменении/удалении комментария."""

    model = Comment
    template_name = "blog/comment.html"
    pk_url_kwarg = "comment_id"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            return redirect("blog:post_detail", pk=self.kwargs.get("post_id"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={
            "pk": self.kwargs["post_id"]})
