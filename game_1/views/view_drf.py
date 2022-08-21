from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from ..forms import *
from ..logic import *
from ..models import *
from ..serializers import *

# //////////////////////////// ApiVIew ////////////////////////////////////////

class WaitingRoomGetUsersAPI(ListAPIView):
    """ Получаем список игроков в typing_room + status_game"""

    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset_users(self):
        req_room_code = self.kwargs['slug']
        select = Players.objects.filter(parent_room__room_code=req_room_code)  # .values_list("player_in_room")
        # получили объект класса Юзер
        select = [s.player_in_room for s in select]
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


class WaitingRoomExitAPI(RoomMixin, APIView):
    """ API Выход из комнаты """

    def get(self, request, *args, **kwargs):
        room_code = kwargs["slug"]
        current_user = request.user
        self.exit_to_game(room_code=room_code)
        return Response({'massage': str(current_user) + " вышел из комнаты " + str(room_code)})


class WaitingRoomJoinAPI(RoomMixin, APIView):
    """ API Войти в комнату """

    def get(self, request, *args, **kwargs):
        room_code = kwargs["slug"]
        current_user = request.user
        self.join_to_game(room_code=room_code)
        return Response({'massage': str(current_user) + " зашел в комнату " + str(room_code)})


class WaitingRoomAddBotAPI(ListAPIView):
    """ Добавить бота в комнату """
    pass


class WaitingTypingRoomGetUsersAPI(RoomMixin, ListAPIView):
    """ Получаем список игроков в typing_room """

    def get_queryset_users(self):
        room_code = self.kwargs['slug']
        current_room = self.get_current_room(room_code=room_code)
        current_round = current_room.round

        # получили объект класса Юзер
        select = AnswerPlayers.objects.filter(answer__isnull=False).filter(
            round_of_answer=current_round).filter(player__parent_room__room_code=room_code)
        select = [s.player.player_in_room for s in select]

        return select

    def list(self, request, *args, **kwargs):
        queryset_users = self.get_queryset_users()
        serializer_users = UserSerializer(queryset_users, many=True)
        return Response({'users': serializer_users.data})
