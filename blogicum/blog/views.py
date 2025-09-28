from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator

from .models import Post, Category, Comment
from .forms import PostForm, ProfileForm, SignUpForm, CommentForm


def paginate(request, queryset, per_page=10):
    """Функция для разбиения на страницы."""
    paginator = Paginator(queryset, per_page)
    page = request.GET.get("page")
    return paginator.get_page(page)


def index(request):
    posts = Post.objects.published()
    page_obj = paginate(request, posts)
    return render(request, "blog/index.html", {"page_obj": page_obj})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.published().filter(category=category)
    page_obj = paginate(request, posts)
    context = {"category": category, "page_obj": page_obj}
    return render(request, "blog/category.html", context)


def profile(request, username):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    profile_owner = get_object_or_404(User, username=username)

    if request.user == profile_owner:
        queryset = profile_owner.posts.all()
    else:
        queryset = profile_owner.posts.published()
    page_obj = paginate(request, queryset)

    context = {"profile_user": profile_owner, "page_obj": page_obj}
    return render(request, "blog/profile.html", context)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("blog:profile", username=user.username)
    else:
        form = SignUpForm()
    return render(request, "registration/registration.html", {"form": form})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/edit_profile.html", {"form": form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if request.method == "POST" and form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/create.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post.id)
    return render(request, "blog/create.html", {"form": form, "post": post})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = None
    if request.user.is_authenticated:
        form = CommentForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("blog:post_detail", post_id=post_id)
    return render(
        request,
        "blog/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)

    form = CommentForm(request.POST or None, instance=comment)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post_id)

    return render(
        request, "blog/edit_comment.html", {"form": form, "comment": comment}
    )


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/confirm_delete.html", {"object": post})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment, pk=comment_id, post_id=post_id, author=request.user
    )
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)
    return render(request, "blog/confirm_delete.html", {"object": comment})