from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('auth/', include('accounts.urls')),
    path('users/', include('users.urls')),
    path('messages/', include('dm.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

