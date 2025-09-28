from django.contrib import admin
from django.urls import path, include
from pages import views as error_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls", namespace="blog")),
    path("auth/", include("django.contrib.auth.urls")),
    path("pages/", include("pages.urls", namespace="pages")),
]

handler404 = error_views.page_not_found
handler500 = error_views.server_error
handler403 = error_views.csrf_failure

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)