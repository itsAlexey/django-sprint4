from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy

from .views import SignUpView, ProfileUpdateView

app_name = "users"

urlpatterns = [
    # Регистрация и профиль
    path("registration/", SignUpView.as_view(), name="registration"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="edit_profile"),

    # Встроенные маршруты авторизации django.contrib.auth
    path("auth/", include("django.contrib.auth.urls")),

    # Изменение и восстановление пароля
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("users:password_change_done")
        ),
        name="password_change",
    ),
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy("users:password_reset_done")
        ),
        name="password_reset",
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("users:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
]