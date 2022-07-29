from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [

    # Логин
    path('register/', RegisterUser.as_view(), name='game_register'),
    path('login/', LoginUser.as_view(), name='game_login'),
    path('logout/', logout_user, name='game_logout'),

    # Игра
    path('', RedirectMainRoomView.as_view(), name='redirect_main_room'),
    path('room/main/', MainRoomView.as_view(), name='main_room'),
    path('room/waiting/', WaitingRoomView.as_view(), name='waiting_room'),
    # path('room/waiting/delete', WaitingRoomDeleteView.as_view(), name='waiting_room_delete'),
    path('room/addbot/', AddBotApiView.as_view(), name='add_bot'),
    path('api/v1/gamers/<slug:slug>/', TempView.as_view(), name='found_gamers'),
    path('room/typing/', TypingRoomView.as_view(), name='typing_room'),
    path('room/waiting/typing/', WaitingTypingRoomView.as_view(), name='waiting_typing_room'),
    path('room/result/', ResultRoomView.as_view(), name='result_room'),
    path('room/gameover/', GamveoverRoomView.as_view(), name='gameover_room'),
    path('find', FindMethodsView.as_view(), name='find'),
    re_path('find2/', FindMethodsSecondView.as_view(), name='find_2'), #/(?P<find_method_2>^)\d+

]