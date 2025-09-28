from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import RegistrationForm, ProfileEditForm

User = get_user_model()


class SignUpView(CreateView):
    """Регистрация нового пользователя + авто-логин."""

    form_class = RegistrationForm
    template_name = "registration/registration_form.html"
    success_url = reverse_lazy("blog:index")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("blog:index")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование данных профиля (только самого себя)."""

    model = User
    form_class = ProfileEditForm
    template_name = "blog/user.html"

    def get_object(self):
        return self.request.user