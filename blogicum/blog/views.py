from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)

from .forms import CommentForm, PostForm, UserForm
from .mixins import CommentChangeMixin, CustomListMixin, PostChangeMixin
from .models import Category, Comment, Post, User


class IndexHome(CustomListMixin, ListView):
    """Главная страница блога: опубликованные посты с прошедшей датой."""

    template_name = "blog/index.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            )
        )


class CategoryListView(CustomListMixin, ListView):
    """Лента постов внутри конкретной категории."""

    template_name = "blog/category.html"

    def get_queryset(self):
        self.category = get_object_or_404(
            Category,
            slug=self.kwargs["category_slug"],
            is_published=True,
        )
        return (
            super()
            .get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
                category__slug=self.kwargs["category_slug"],
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class ProfileView(CustomListMixin, ListView):
    """Страница профиля пользователя."""

    template_name = "blog/profile.html"

    def get_queryset(self):
        self.author = get_object_or_404(User,
                                        username=self.kwargs["username"])
        base_qs = super().get_queryset().filter(author=self.author)
        if self.author != self.request.user:
            return base_qs.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            )
        return base_qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.author
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля текущего пользователя."""

    model = User
    form_class = UserForm
    template_name = "blog/user.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("blog:profile", kwargs={"username": self.request.user})


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание новой публикации."""

    model = Post
    form_class = PostForm
    template_name = "blog/create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("blog:profile", kwargs={"username": self.request.user})


class PostUpdateView(LoginRequiredMixin, PostChangeMixin, UpdateView):
    """Редактирование поста."""

    form_class = PostForm

    def get_success_url(self):
        return reverse("blog:post_detail",
                       kwargs={"pk": self.kwargs["post_id"]})


class PostDeleteView(LoginRequiredMixin, PostChangeMixin, DeleteView):
    """Удаление поста."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Используем форму для вывода полей поста (read-only в шаблоне)
        context["form"] = PostForm(instance=self.object)
        return context

    def get_success_url(self):
        return reverse("blog:profile", kwargs={"username": self.request.user})


class PostDetailView(DetailView):
    """
    Страница отдельной публикации.
    Свой пост доступен всегда; чужой — только если опубликован и не отложен.
    """

    model = Post
    template_name = "blog/detail.html"
    pk_url_kwarg = "pk"

    def get_object(self, queryset=None):
        base_qs = self.model.objects.select_related(
            "location", "category", "author")
        obj = super().get_object(queryset=base_qs)
        if obj.author != self.request.user:
            obj = get_object_or_404(
                base_qs.filter(
                    pub_date__lte=timezone.now(),
                    category__is_published=True,
                    is_published=True,
                ),
                pk=self.kwargs["pk"],
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related("author")
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария к посту."""

    model = Comment
    form_class = CommentForm
    pk_url_kwarg = "post_id"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get(
            "post_id"))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("blog:post_detail", kwargs={
            "pk": self.kwargs.get("post_id")})


class CommentUpdateView(LoginRequiredMixin, CommentChangeMixin, UpdateView):
    """Редактирование комментария."""

    form_class = CommentForm


class CommentDeleteView(LoginRequiredMixin, CommentChangeMixin, DeleteView):
    """Удаление комментария."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Удаляем form из контекста, если она вдруг появилась
        context.pop("form", None)
        return context
