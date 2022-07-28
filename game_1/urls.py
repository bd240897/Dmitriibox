from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [

    # Логин
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),

    # Игра
    path('room/main/', MainRoomView.as_view(), name='main_room'),
    path('room/waiting/', WaitingRoomView.as_view(), name='waiting_room'),
    path('room/addbot/', AddBotApiView.as_view(), name='add_bot'),
    path('api/v1/gamers/<slug:slug>/', TempView.as_view(), name='found_gamers'),
    path('room/typing/', TypingRoomView.as_view(), name='typing_room'),
    path('room/waiting/typing/', WaitingTypingRoomView.as_view(), name='waiting_typing_room'),
    path('room/result/', ResultRoomView.as_view(), name='result_room'),

]