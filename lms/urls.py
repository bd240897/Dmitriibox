# chat/urls.py
from django.urls import path, include, re_path
from lms.views import *

urlpatterns = [
    path('find/', FindUserView.as_view(), name='find'),
    path('upload/', AvatarUploadView.as_view(), name='upload'),
]

