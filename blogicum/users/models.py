from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    """Расширенная стандартная модель пользователя."""

    def get_absolute_url(self):
        return reverse("blog:profile", kwargs={"username": self.username})
