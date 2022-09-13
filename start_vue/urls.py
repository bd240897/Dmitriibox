# chat/urls.py
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views.views import *

router = DefaultRouter()
router.register(r'game', GameRoomViewSet, basename='game_room')
# print(router.urls)

urlpatterns = [
    ################# ТЕСТИРУЮ ViewSet ######################
    path('', include(router.urls)),
    ################# index.html ######################
    re_path(r'^.*', IndexView.as_view(), name='index'),
]

