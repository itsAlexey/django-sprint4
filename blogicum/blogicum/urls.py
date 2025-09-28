from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler403 = 'pages.views.permission_denied'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('auth/', include('django.contrib.auth.urls')),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
