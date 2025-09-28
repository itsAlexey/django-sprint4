from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # Главная страница
    path("", views.IndexView.as_view(), name="index"),

    # Просмотр постов
    path("posts/<int:post_id>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/create/", views.PostCreateView.as_view(), name="create_post"),
    path("posts/<int:post_id>/edit/", views.PostUpdateView.as_view(), name="edit_post"),
    path("posts/<int:post_id>/delete/", views.PostDeleteView.as_view(), name="delete_post"),

    # Работа с комментариями
    path("posts/<int:post_id>/comment/", views.CommentCreateView.as_view(), name="add_comment"),
    path(
        "posts/<int:post_id>/comment/<int:comment_id>/edit/",
        views.CommentUpdateView.as_view(),
        name="edit_comment",
    ),
    path(
        "posts/<int:post_id>/comment/<int:comment_id>/delete/",
        views.CommentDeleteView.as_view(),
        name="delete_comment",
    ),

    # Просмотр категорий
    path("category/<slug:category_slug>/", views.CategoryView.as_view(), name="category_posts"),

    # Профили пользователей
    path("profile/<str:username>/", views.ProfileView.as_view(), name="profile"),
]