from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from ..forms import *
from ..logic import *
from ..models import *
from ..serializers import *

# //////////////////////////// ApiVIew ////////////////////////////////////////

class GameStatusApi(RetrieveAPIView):
    """ Получить текущий статус комнаты """

    serializer_class = GameStatusSerializer
    queryset = GameRoom.objects.all()
    lookup_field = 'room_code'
    lookup_url_kwarg = 'slug'

class WaitingRoomGetUsersAPI(ListAPIView):
    """ Получаем список игроков в typing_room + status_game"""

    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset_users(self):
        req_room_code = self.kwargs['slug']
        select = User.objects.filter(game_players__room_code=req_room_code)
        print("select", select)
        return select

    def get_queryset_gameroom(self):
        req_room_code = self.kwargs['slug']
        select = GameRoom.objects.get(room_code=req_room_code)
        return select

    def list(self, request, *args, **kwargs):
        # https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/generic-views

        queryset_users = self.get_queryset_users()
        serializer_users = UserSerializer(queryset_users, many=True)
        queryset_gameroom = self.get_queryset_gameroom()
        serializer_gameroom = GameRoomSerializer(queryset_gameroom, many=False)
        return Response({'users': serializer_users.data, 'gameroom': serializer_gameroom.data})

class WaitingTypingRoomGetUsersAPI(RoomMixin, ListAPIView):
    """ Получаем список игроков в typing_room """

    def get_queryset_users(self):
        room_code = self.kwargs['slug']
        current_room = self.get_current_room()
        current_round = current_room.round

        # получили объект класса Юзер
        select = AnswerPlayers.objects\
            .filter(answer__isnull=False,round_of_answer=current_round)\
            .filter(room__room_code=room_code)
        # TODO мб использовать values_list()
        select = [s.player for s in select]
        return select

    def list(self, request, *args, **kwargs):
        queryset_users = self.get_queryset_users()
        serializer_users = UserSerializer(queryset_users, many=True)
        return Response({'users': serializer_users.data})

class WaitingRoomExitAPI(RoomMixin, APIView):
    """ API Выход из комнаты """

    def get(self, request, *args, **kwargs):
        self.current_room.exit_to_game(self.request, self.current_user)
        return Response({'massage': str(self.current_user) + " вышел из комнаты " + str(self.room_code)})


class WaitingRoomJoinAPI(RoomMixin, APIView):
    """ API Войти в комнату """

    def get(self, request, *args, **kwargs):
        self.current_room.join_to_game(self.request, self.current_user)
        return Response({'massage': str(self.current_user) + " зашел в комнату " + str(self.room_code)})


class WaitingRoomAddBotAPI(ListAPIView):
    """ Добавить бота в комнату """
    pass



