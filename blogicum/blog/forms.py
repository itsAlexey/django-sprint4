from django import forms

from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    """Форма создания/редактирования публикации без ручного выбора автора."""

    class Meta:
        model = Post
        exclude = ("author",)
        widgets = {
            "pub_date": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={"type": "datetime-local"}
            ),
        }


class CommentForm(forms.ModelForm):
    """Форма комментария к посту."""

    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(
                attrs={"rows": 5, "cols": 60,
                       "placeholder": "Напишите комментарий..."}
            )
        }


class UserForm(forms.ModelForm):
    """Редактирование профиля пользователя."""

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
