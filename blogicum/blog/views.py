from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
# Декоратор, который ограничивает доступ к view-функции только для авторизованных пользователей.
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Post, Category

# Константа для количества постов на главной странице
POSTS_ON_MAIN_PAGE = 5


def index(request):
    last_posts = Post.objects.select_related('category').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:POSTS_ON_MAIN_PAGE]
    return render(request, 'blog/index.html', {'post_list': last_posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('category').filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        ),
        pk=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    # Сначала проверяем, существует ли опубликованная категория с таким slug
    category = get_object_or_404(
        Category, 
        slug=category_slug, 
        is_published=True
    )
    
    # Затем получаем посты для этой категории
    post_list = Post.objects.select_related('category').filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category=category
    ).order_by('-pub_date')
    
    return render(
        request,
        'blog/category.html',
        {'category': category, 'post_list': post_list}
    )


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user)  # Получили публикации юзера

    context = {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        # Здесь будет обработка формы редактирования
        pass
    return render(request, 'profile_edit.html')
