from django import forms
from django.utils import timezone

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Форма для добавления и редактирования публикаций."""

    pub_date = forms.DateTimeField(
        label="Дата публикации",
        required=True,
        initial=timezone.now,
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
        help_text="Выберите дату. В будущем — отложенная публикация.",
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
    """Форма для комментариев."""

    class Meta:
        model = Comment
        fields = ("text",)
        labels = {"text": "Напишите комментарий"}
