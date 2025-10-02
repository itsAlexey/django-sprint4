from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy

from .views import UserRegisterView, UserProfileEditView

app_name = "users"

urlpatterns = [
    path(
        "auth/password_change/",
        auth_views.PasswordChangeView.as_view(
            success_url=reverse_lazy("users:password_change_done")
        ),
        name="password_change",
    ),
    path(
        "auth/password_reset/",
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy("users:password_reset_done")
        ),
        name="password_reset",
    ),
    path(
        "auth/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("users:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "auth/registration/",
        UserRegisterView.as_view(),
        name="registration",
    ),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "profile/edit/",
        UserProfileEditView.as_view(),
        name="edit_profile",
    ),
]
