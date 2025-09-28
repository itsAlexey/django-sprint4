from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import PostForm, CommentForm
from .models import Post, Comment, Category, User
from .mixins import PostBaseMixin, CommentBaseMixin
from .utils import filter_published_posts


# Количество записей на страницу (пагинация)
POSTS_PER_PAGE = 10


class PostCreateView(LoginRequiredMixin, PostBaseMixin, CreateView):
    """Создание нового поста (только авторизованным)."""

    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:profile", args=[self.request.user.username])


class PostUpdateView(LoginRequiredMixin, PostBaseMixin, UpdateView):
    """Редактирование поста (только автор = хозяин)."""

    form_class = PostForm

    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        if post.author != self.request.user:
            return redirect("blog:post_detail", post_id=post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post_detail", args=[self.kwargs["post_id"]])


class PostDeleteView(LoginRequiredMixin, PostBaseMixin, DeleteView):
    """Удаление поста (подтверждение + проверка владельца)."""

    success_url = reverse_lazy("blog:index")

    def delete(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        if post.author != self.request.user:
            return redirect("blog:post_detail", post_id=post.pk)
        return super().delete(request, *args, **kwargs)


class PostDetailView(PostBaseMixin, DetailView):
    """Деталка поста с комментами."""

    template_name = "blog/detail.html"

    def get_object(self, queryset=None):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        if post.author == self.request.user:
            return post
        return get_object_or_404(
            filter_published_posts(Post.objects.all()), pk=post.pk
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.get_object().comments.select_related("author")
        return context


class CommentCreateView(LoginRequiredMixin, CommentBaseMixin, CreateView):
    """Добавление комментария к посту."""

    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, CommentBaseMixin, UpdateView):
    """Редактирование комментария (только автор)."""

    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs["comment_id"])
        if comment.author != self.request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(LoginRequiredMixin, CommentBaseMixin, DeleteView):
    """Удаление комментария (подтверждение)."""

    def delete(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs["comment_id"])
        if comment.author != self.request.user:
            return redirect("blog:post_detail", post_id=self.kwargs["post_id"])
        return super().delete(request, *args, **kwargs)


class IndexView(ListView):
    """Главная страница со списком постов."""

    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        return filter_published_posts(Post.objects.all())


class CategoryView(ListView):
    """Посты внутри выбранной категории."""

    model = Post
    template_name = "blog/category.html"
    context_object_name = "posts"
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        category_slug = self.kwargs["category_slug"]
        category = get_object_or_404(Category, slug=category_slug, is_published=True)
        return filter_published_posts(category.posts.all())


class ProfileView(ListView):
    """Профиль пользователя (все его посты)."""

    model = Post
    template_name = "blog/profile.html"
    context_object_name = "posts"
    paginate_by = POSTS_PER_PAGE

    def get_queryset(self):
        author = get_object_or_404(User, username=self.kwargs["username"])
        posts = author.posts.all()
        if self.request.user != author:
            posts = filter_published_posts(posts)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = get_object_or_404(User, username=self.kwargs["username"])
        return context
