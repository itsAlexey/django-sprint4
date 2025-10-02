from django.urls import reverse_lazy

from .models import Post, Comment


class PostFormMixin:
    """Общий миксин для работы с постами."""

    model = Post
    template_name = "blog/create.html"
    pk_url_kwarg = "post_id"


class CommentFormMixin:
    """Общий миксин для комментариев."""

    model = Comment
    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"

    def get_success_url(self):
        return reverse_lazy("blog:post_detail", kwargs={
            "post_id": self.kwargs["post_id"]})
