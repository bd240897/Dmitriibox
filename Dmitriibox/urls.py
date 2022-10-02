"""Dmitriibox URL Configuration"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
# from Dmitriibox import settings
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game_1.urls')),
    path('vue/', include('game_1_vue.urls')),
    path('vuestart/', include('start_vue.urls')),
]

# REST FRAMEWORK
urlpatterns_drf = [
    path('api/v1/drf-auth/', include('rest_framework.urls')),
]

# DJOSER
urlpatterns_djoser = [
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

# add new url
urlpatterns += urlpatterns_drf
urlpatterns += urlpatterns_djoser
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)