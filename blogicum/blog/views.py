from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .forms import PostForm, CommentForm
from .models import Post, Category, Comment, User
from .utils import published_posts
from .mixins import PostFormMixin, CommentFormMixin

PAGINATE = 10


class IndexView(ListView):
    """Главная страница с лентой постов."""

    template_name = "blog/index.html"
    paginate_by = PAGINATE
    model = Post
    context_object_name = "post_list"

    def get_queryset(self):
        return published_posts(Post.objects)


class CategoryView(ListView):
    """Посты из категории."""

    template_name = "blog/category.html"
    paginate_by = PAGINATE

    def get_queryset(self):
        category = get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=True
        )
        return published_posts(category.posts)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category, slug=self.kwargs["category_slug"]
        )
        return context


class ProfileView(ListView):
    """Профиль пользователя с публикациями."""

    model = Post
    template_name = "blog/profile.html"
    paginate_by = PAGINATE
    context_object_name = "profile_posts"

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs["username"])
        posts = author.posts.all()
        if self.request.user != author:
            posts = published_posts(posts)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = get_object_or_404(
            User,
            username=self.kwargs["username"])
        return context


class PostDetailView(DetailView):
    """Подробная страница поста."""

    template_name = "blog/detail.html"
    pk_url_kwarg = "post_id"
    model = Post

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        if self.request.user == post.author:
            return post
        return get_object_or_404(published_posts(Post.objects), pk=post.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.get_object().comments.select_related(
            "author")
        return context


class PostCreateView(LoginRequiredMixin, PostFormMixin, CreateView):
    """Создание поста."""

    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:profile", args=[self.request.user.username])


class PostUpdateView(LoginRequiredMixin, PostFormMixin, UpdateView):
    """Редактирование поста."""

    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["post_id"])
        if post.author != request.user:
            return redirect("blog:post_detail", post_id=post.id)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post_detail", args=[self.kwargs["post_id"]])


class PostDeleteView(LoginRequiredMixin, PostFormMixin, DeleteView):
    """Удаление поста."""

    success_url = reverse_lazy("blog:index")

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs["post_id"])
        if post.author != request.user:
            return redirect("blog:index")
        return super().delete(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, CommentFormMixin, CreateView):
    """Создание комментария."""

    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, CommentFormMixin, UpdateView):
    """Редактирование комментария."""

    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs["comment_id"])
        if comment.author != request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, CommentFormMixin, DeleteView):
    """Удаление комментария."""

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs["comment_id"])
        if comment.author != request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().delete(request, *args, **kwargs)
