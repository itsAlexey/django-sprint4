from django import forms
from django.utils import timezone

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Форма для поста."""

    pub_date = forms.DateTimeField(
        initial=timezone.now,
        required=True,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    class Meta:
        model = Post
        fields = (
            "title",
            "image",
            "text",
            "pub_date",
            "location",
            "category",
            "is_published",
        )


class CommentForm(forms.ModelForm):
    """Форма для комментария."""

    class Meta:
        model = Comment
        fields = ("text",)
