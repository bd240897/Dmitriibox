import json

from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet

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
        select = AnswerPlayers.objects \
            .filter(answer__isnull=False, round_of_answer=current_round) \
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


# //////////////////////////// URL FOR VUE ////////////////////////////////////////

# TODO не используется удалить?
class WaitingRoomAPI(RoomMixin, APIView):
    """ API """

    ACTION = {"next_room": "NEXT_ROOM",
              "start_game": "START_GAME"}

    name_current_view_room = 'waiting_room'

    # def get(self, request, *args, **kwargs):
    #     return Response({'massage': str(self.current_user) + " зашел в комнату " + str(self.room_code),
    #                      'next_url': reverse("typing_room", kwargs={'slug': self.room_code})
    #                      })

    def post(self, request, *args, **kwargs):

        # https://proproprogs.ru/django/drf-bazovyy-klass-apiview-dlya-predstavleniy
        action = request.data['action']  # {"action": "START_GAME"}
        if action == "START_GAME":
            # TODO registration for vue
            # self.current_room.switch_game_status(self.request, self.current_user, "typing_room")
            return Response({'massage': "Got msg " + action,
                             'next_url': reverse("typing_room", kwargs={'slug': self.room_code})
                             })
        else:
            return Response({'error': "undefined action",
                             })


################# ТЕСТИРУЮ ViewSet ######################
class GameRoomViewSet(RoomMixin, ModelViewSet):
    queryset = GameRoom.objects.all()
    serializer_class = GameRoomVueSerializer

    ########## waiting_room ##########
    # /game/start/
    @action(methods=['get'], detail=False, url_path='start')
    def vs_start_game(self, request):
        return Response({'massage': "vs_start_game"})

    # /game/start/
    @action(methods=['get'], detail=False, url_path='delete')
    def vs_delete_room(self, request):
        return Response({'massage': "vs_delete_game"})

    ########## waiting_room ##########
    @action(methods=['get'], detail=False, url_path='room/waiting')
    def vs_waiting_room(self, request):
        return Response({'massage': "vs_waiting_room"})

    ########## typing_room ##########
    # /game/room/typing/
    # vs_post_answer
    @action(methods=['post'], detail=False, url_path='room/typing')
    def vs_typing_room(self, request):
        current_user = self.request.user
        if current_user.is_anonymous:
            return Response({'error': "User is anonymous"})

        name_current_view_room = 'typing_room'
        answer = request.data.get('answer')
        room_code = request.data.get('room_code')

        current_room = GameRoom.objects.get(room_code=room_code)

        current_room.switch_game_status(self.request, current_user, name_current_view_room)
        AnswerPlayers.objects.create(player=current_user,
                                     answer=answer,
                                     round_of_answer=current_room.round,
                                     room=current_room)

        return Response({'success': "Massage sent",
                         'massage': "vs_typing_room",
                         'echo': JSONRenderer().render(dict(request.data))})

    ########## waiting_typing_room ##########
    # /game/room/typing/
    @action(methods=['post'], detail=False, url_path='room/waiting/typing')
    def vs_waiting_typing_room(self, request):
        return Response({'massage': "vs_waiting_typing_room"})

    ########## result_room ##########
    # /game/room/result/
    @action(methods=['get'], detail=False, url_path='room/result')
    def vs_result_room(self, request):
        return Response({'massage': "vs_result_room"})

    ########## result_list_room ##########
    # /game/room/result/list
    @action(methods=['get'], detail=False, url_path='room/result/list')
    def vs_result_list_room(self, request):
        return Response({'massage': "vs_result_list_room"})
