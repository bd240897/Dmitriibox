# chat/urls.py
from django.urls import path, include, re_path
from .views.views import *

urlpatterns = [
    re_path(r'^.*', IndexView.as_view(), name='index'),
]

