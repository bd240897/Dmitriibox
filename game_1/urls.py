from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

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
    path('rejoin/<slug:slug>/', RejoinGameView.as_view(), name='rejoin_game'),
    path('waiting/<slug:slug>/', WaitingRoomTestView.as_view(), name='waiting_room'),
    path('typing/<slug:slug>/', TypingRoomView.as_view(), name='typing_room'),
    path('waiting/typing/<slug:slug>/', WaitingTypingRoomView.as_view(), name='waiting_typing_room'),
    path('result/<slug:slug>/', ResultRoomView.as_view(), name='result_room'),
    path('result/list/<slug:slug>/', ResultListView.as_view(), name='result_list_room'),
    path('gameover/<slug:slug>/', GamveoverRoomView.as_view(), name='gameover_room'),
]

router = DefaultRouter()
router.register(r'game', GameRoomViewSet, basename='game_room')
print(router.urls)

urlpatterns_drf = [
    # ///////////////// ApiView ИГРА /////////////////////
    path('gamestatus/<slug:slug>/', GameStatusApi.as_view(), name='game_status_API'),
    path('waiting/<slug:slug>/gatusers/', WaitingRoomGetUsersAPI.as_view(),
         name='waiting_room_API_gatusers'),
    path('waiting/typing/<slug:slug>/gatusers/', WaitingTypingRoomGetUsersAPI.as_view(),
         name='waiting_typing_room_API_gatusers'),
    path('waiting/<slug:slug>/exit/', WaitingRoomExitAPI.as_view(), name='waiting_room_API_exit'),
    path('waiting/<slug:slug>/join/', WaitingRoomJoinAPI.as_view(), name='waiting_room_API_join'),
    path('waiting/<slug:slug>/addbot/', WaitingRoomAddBotAPI.as_view(), name='ting_room_api_addbot'),

    ####### URL FOR VUE ########
    # Start
    path('waiting/<slug:slug>/', WaitingRoomAPI.as_view(), name='waiting_room_API'),
]



urlpatterns_test = [
    # ///////////////// TEST /////////////////////
    path('find/<slug:slug>', FindMethodsView.as_view(), name='find'),
    re_path('test/', TestView.as_view(), name='test'), #/(?P<find_method_2>^)\d+
    path('test-page/', WaitingRoomTestView.as_view(), name='test-page'),
]

urlpatterns = [
    path('', include(urlpatterns_login)),
    path('', RedirectMainRoomView.as_view(), name='redirect_main_room'),
    path('room/', include(urlpatterns_room)),
    path('api/v1/room/', include(urlpatterns_drf)),
    path('', include(urlpatterns_test)),

    ################# ТЕСТИРУЮ ViewSet ######################
    path('', include(router.urls)),
]
