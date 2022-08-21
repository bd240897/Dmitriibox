from django.contrib import admin
from django.urls import path, include, re_path
from .views.views import *

urlpatterns_login = [
    # ///////////////// ЛОГИН /////////////////////
    path('register/', RegisterUser.as_view(), name='game_register'),
    path('login/', LoginUser.as_view(), name='game_login'),
    path('logout/', logout_user, name='game_logout'),
]

urlpatterns_room = [
    # ///////////////// DjangoView ИГРА /////////////////////
    path('main/', MainRoomView.as_view(), name='main_room'),
    path('waiting/<slug:slug>/', WaitingRoomTestView.as_view(), name='waiting_room'),
    # path('room/waiting/delete', WaitingRoomDeleteView.as_view(), name='waiting_room_delete'),
    path('typing/<slug:slug>/', TypingRoomView.as_view(), name='typing_room'),
    path('waiting/typing/<slug:slug>/', WaitingTypingRoomView.as_view(), name='waiting_typing_room'),
    path('result/<slug:slug>/', ResultRoomView.as_view(), name='result_room'),
    path('gameover/', GamveoverRoomView.as_view(), name='gameover_room'),
]

urlpatterns_drf = [
    # ///////////////// ApiView /////////////////////
    path('gamers/<slug:slug>/', TempView.as_view(), name='found_gamers'),
    path('waiting/<slug:slug>/gatusers/', WaitingRoomGetUsersAPI.as_view(),
         name='waiting_room_api_gatusers'),
    path('waiting/<slug:slug>/exit/', WaitingRoomExitAPI.as_view(), name='waiting_room_api_exit'),
    path('waiting/<slug:slug>/join/', WaitingRoomJoinAPI.as_view(), name='waiting_room_api_join'),
    path('waiting/<slug:slug>/addbot/', WaitingRoomAddBotAPI.as_view(), name='ting_room_api_addbot'),
    path('waiting/typing/<slug:slug>/gatusers/', WaitingTypingRoomGetUsersAPI.as_view(),
         name='waiting_typing_room_api_gatusers'),
]

urlpatterns_test = [
    # ///////////////// TEST /////////////////////
    path('find/<slug:slug>', FindMethodsView.as_view(), name='find'),
    re_path('find2/', FindMethodsSecondView.as_view(), name='find_2'), #/(?P<find_method_2>^)\d+
    path('test-page/', WaitingRoomTestView.as_view(), name='test-page'),
    # path('test-api/', GetCurrentUsersAPI.as_view(), name='test-api'),
    # path('test-api/<slug:slug>', GetCurrentUsersAPI.as_view(), name='test-api'),
]

urlpatterns = [
    path('', include(urlpatterns_login)),
    path('', RedirectMainRoomView.as_view(), name='redirect_main_room'),
    path('room/', include(urlpatterns_room)),
    path('api/v1/room/', include(urlpatterns_drf)),
    path('', include(urlpatterns_test)),
]
