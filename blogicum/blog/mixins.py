from django.urls import reverse
from .models import Post, Comment


class PostBaseMixin:
    """Общий миксин для работы с постами."""

    model = Post
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"


class CommentBaseMixin:
    """Общий миксин для работы с комментариями."""

    model = Comment
    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"

    def get_success_url(self):
        return reverse("blog:post_detail", args=[self.kwargs["post_id"]])