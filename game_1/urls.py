from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [

    # Логин
    path('register/', RegisterUser.as_view(), name='game_register'),
    path('login/', LoginUser.as_view(), name='game_login'),
    path('logout/', logout_user, name='game_logout'),

    # Игра
    # ///////////////// DjangoView /////////////////////
    path('', RedirectMainRoomView.as_view(), name='redirect_main_room'),
    path('room/main/', MainRoomView.as_view(), name='main_room'),
    path('room/waiting/<slug:slug>/', WaitingRoomTestView.as_view(), name='waiting_room'),
    # path('room/waiting/delete', WaitingRoomDeleteView.as_view(), name='waiting_room_delete'),
    path('api/v1/gamers/<slug:slug>/', TempView.as_view(), name='found_gamers'),
    path('room/typing/<slug:slug>/', TypingRoomView.as_view(), name='typing_room'),
    path('room/waiting/typing/<slug:slug>/', WaitingTypingRoomView.as_view(), name='waiting_typing_room'),
    path('room/result/<slug:slug>/', ResultRoomView.as_view(), name='result_room'),
    path('room/gameover/', GamveoverRoomView.as_view(), name='gameover_room'),
    # ///////////////// ApiView /////////////////////
    path('api/v1/room/waiting/<slug:slug>/gatusers/', WaitingRoomGetUsersAPI.as_view(), name='waiting_room_api_gatusers'),
    path('api/v1/room/waiting/<slug:slug>/exit/', WaitingRoomExitAPI.as_view(), name='waiting_room_api_exit'),
    path('api/v1/room/waiting/<slug:slug>/join/', WaitingRoomJoinAPI.as_view(), name='waiting_room_api_join'),
    path('api/v1/room/waiting/<slug:slug>/addbot/', WaitingRoomAddBotAPI.as_view(), name='ting_room_api_addbot'),
    path('api/v1/room/waiting/typing/<slug:slug>/gatusers/', WaitingTypingRoomGetUsersAPI.as_view(), name='waiting_typing_room_api_gatusers'),

    # тесты
    path('find/<slug:slug>', FindMethodsView.as_view(), name='find'),
    re_path('find2/', FindMethodsSecondView.as_view(), name='find_2'), #/(?P<find_method_2>^)\d+
    path('test-page/', WaitingRoomTestView.as_view(), name='test-page'),
    # path('test-api/', GetCurrentUsersAPI.as_view(), name='test-api'),
    # path('test-api/<slug:slug>', GetCurrentUsersAPI.as_view(), name='test-api'),
]