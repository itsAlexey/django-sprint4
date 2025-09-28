from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegistrationForm(UserCreationForm):
    """Форма регистрации нового пользователя."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")


class ProfileEditForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя."""

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        labels = {
            "username": "Логин",
            "email": "Электронная почта",
            "first_name": "Имя",
            "last_name": "Фамилия",
        }
