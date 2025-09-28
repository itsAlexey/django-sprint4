from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

from .forms import RegistrationForm, ProfileForm, PostForm, CommentForm
from .models import Post, Category, Comment

User = get_user_model()


def paginate(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def index(request):
    posts = Post.objects.filter(is_published=True, pub_date__lte=timezone.now())
    return render(request, "blog/index.html", {"page_obj": paginate(request, posts)})


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(is_published=True, pub_date__lte=timezone.now())
    return render(request, "blog/category.html", {
        "category": category,
        "page_obj": paginate(request, posts),
    })


def profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        posts = user.posts.all()
    else:
        posts = user.posts.filter(is_published=True, pub_date__lte=timezone.now())
    return render(request, "blog/profile.html", {
        "profile_user": user,
        "page_obj": paginate(request, posts),
    })


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("blog:profile", username=user.username)
    else:
        form = RegistrationForm()
    return render(request, "registration/registration.html", {"form": form})


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/edit_profile.html", {"form": form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/create.html", {"form": form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect("blog:post_detail", post_id=post.id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post.id)
    return render(request, "blog/create.html", {"form": form, "post": post})


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comments.all()
    form = CommentForm(request.POST or None) if request.user.is_authenticated else None
    if request.user.is_authenticated and request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect("blog:post_detail", post_id=post.id)
    return render(request, "blog/detail.html", {"post": post, "comments": comments, "form": form})


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id)
    if comment.author != request.user:
        return redirect("blog:post_detail", post_id=post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect("blog:post_detail", post_id=post_id)
    return render(request, "blog/edit_comment.html", {"form": form, "comment": comment})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile", username=request.user.username)
    return render(request, "blog/confirm_delete.html", {"object": post})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, post_id=post_id, author=request.user)
    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", post_id=post_id)
    return render(request, "blog/confirm_delete.html", {"object": comment})