from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    """Кастомная модель пользователя: расширяем стандартный AbstractUser."""

    def get_absolute_url(self):
        """Ссылка на профиль пользователя."""
        return reverse("blog:profile", kwargs={"username": self.username})
