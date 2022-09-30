import json
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet
from game_1.logic import *
from game_1.models import *
from game_1.serializers import *


################# ТЕСТИРУЮ ViewSet ######################

class GameRoomViewSet(RoomMixin, ModelViewSet):
    queryset = GameRoom.objects.all()
    serializer_class = GameRoomVueSerializer

    ########## COMMON ##########
    # /game/gamestatus/
    @action(methods=['get'], detail=False, url_path='status')
    def vs_get_status_room(self, request):
        room_code = request.data.get('room_code')
        # проверка отправили ли кож комнаты

        # проверка существует ли комната
        if not GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'massage': f"Комнаты {room_code} не существует!!!!"})

        status = GameRoom.objects.get(room_code=room_code).status
        return Response({'massage': f"Статус игры {room_code}: {status}"})

    # /game/switch/status/
    @action(methods=['get'], detail=False, url_path='switch/status')
    def vs_switch_status_room(self, request):

        # TODO этот код дублируется в model switch_game_status
        room_code = request.data.get('room_code')
        current_room = GameRoom.objects.get(room_code=room_code)
        if not current_room.is_user_owner(self.request.user):
            return Response(
                {'massage': f"Пользователь {self.request.user} не создатель комнаты {room_code}"})

        new_status = request.data.get('new_status')
        ALLOWED_STATUS = [i[0] for i in GameRoom.CHOICES]
        if new_status not in ALLOWED_STATUS:
            return Response({'massage': f"Статуса {new_status} не существует!"})

        current_room.switch_game_status(self.request, self.request.user, new_status)
        return Response({'massage': f"Статус игры {room_code} изменен на {new_status}"})

    # /game/create/
    @action(methods=['post'], detail=False, url_path='create')
    def vs_create_room(self, request):
        room_code = request.data.get('room_code')

        # пользователь не вошел
        if self.request.user.is_anonymous:
            return Response({'error': "User is anonymous"})

        # игра уже существует
        if GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'error': f"Комната {room_code} уже существует!",
                             'next_room': f"Переход в комнату ожидания"})
            # TODO если существует то пустить в суще-ую комнату
        # создадим игру (комнату)
        else:
            # создает новую игру status = 'main_room'
            object = GameRoom.objects.create(room_code=room_code,
                                             owner=self.request.user,
                                             status='waiting_room')
            # добавим сразу в комнату owners
            object.players.add(self.request.user)
            return Response({'success': f"Была создана комната {room_code}"})

    ########## waiting_room ##########

    # /game/players/
    @action(methods=['get'], detail=False, url_path='players')
    def vs_players_room(self, request):
        # room_code = request.data.get('room_code')
        room_code = request.query_params.get('room_code')
        if not GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'error': f"Комнаты {room_code} не существует!"})

        queryset = User.objects.filter(game_players__room_code=room_code)
        serializer = UserSerializer(queryset, many=True)
        return Response({'players': serializer.data})

    # /game/delete/
    @action(methods=['get'], detail=False, url_path='delete')
    def vs_delete_room(self, request):
        room_code = request.query_params.get('room_code')

        if not GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'error': f"Комнаты {room_code} не существует!"})

        current_room = GameRoom.objects.get(room_code=room_code)
        current_room.delete()
        return Response({'success': f"Комната {room_code} удалена!"})

    # /game/join/
    @action(methods=['get'], detail=False, url_path='join')
    def vs_join_room(self, request):
        room_code = request.query_params.get('room_code')

        # пользователь не вошел
        if self.request.user.is_anonymous:
            return Response({'error': "User is anonymous"})

        # проверка существует ли комната
        if not GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'error': f"Комнаты {room_code} не существует!"})

        current_room = GameRoom.objects.get(room_code=room_code)
        if current_room.is_user_in_room(self.request.user):
            return Response({'error': f"{self.request.user} уже есть в комнате {room_code}"})

        current_room.join_to_game(self.request, self.request.user)
        return Response({'success': f"{self.request.user} зашел в комнату {room_code}"})

    # /game/exit/
    @action(methods=['get'], detail=False, url_path='exit')
    def vs_exit_room(self, request):
        room_code = request.query_params.get('room_code')

        # пользователь не вошел
        if self.request.user.is_anonymous:
            return Response({'error': "User is anonymous"})

        # проверка существует ли комната
        if not GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'error': f"Комнаты {room_code} не существует!"})

        current_room = GameRoom.objects.get(room_code=room_code)
        if not current_room.is_user_in_room(self.request.user):
            return Response({'error': str(self.request.user) + " нет в комнате " + str(room_code)})

        current_room.exit_to_game(self.request, self.request.user)
        return Response({'success': f"{self.request.user} вышел из комнаты {room_code}"})

    ########## typing_room ##########

    # /game/question/
    @action(methods=['get'], detail=False, url_path='question')
    def vs_get_questions(self, request):
        room_code = request.query_params.get('room_code')

        # проверка существует ли комната
        if not GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'error': f"Комнаты {room_code} не существует!"})

        current_round = GameRoom.objects.get(room_code=room_code).round
        queryset = Questions.objects.get(round_for_question=current_round)
        serializer = QuestionsSerializer(queryset)

        return Response({'massage': serializer.data})

    # /game/send/
    # vs_post_answer
    @action(methods=['post'], detail=False, url_path='send')
    def vs_typing_room(self, request):
        name_current_view_room = 'typing_room'
        answer = request.data.get('answer')
        room_code = request.data.get('room_code')
        print(answer)

        if self.request.user.is_anonymous:
            return Response({'error': "User is anonymous"})

        # проверка существует ли комната
        if not GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'error': f"Комнаты {room_code} не существует!"})

        # проверка существует ли комната
        if not answer:
            return Response({'error': "Поле answer пустое или не существует"})

        current_room = GameRoom.objects.get(room_code=room_code)

        current_room.switch_game_status(self.request, self.request.user, name_current_view_room)
        AnswerPlayers.objects.create(player=self.request.user,
                                     answer=answer,
                                     round_of_answer=current_room.round,
                                     room=current_room)
        # TODO начать использовать f-строки везде
        # https://python-scripts.com/f-strings
        return Response({'success': f"Cообщение пользователя {self.request.user} на раунд {current_room.round} для игры {room_code} записано!",
                         'next_room': f"Переход в комнату ожидания #2"})

    ########## waiting_typing_room ##########

    # /game/tying/players/
    @action(methods=['get'], detail=False, url_path='tying/players')
    def vs_typing_players_room(self, request):
        room_code = request.query_params.get('room_code')
        current_room = GameRoom.objects.get(room_code=room_code)
        current_round = current_room.round
        if not GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'error': f"Комнаты {room_code} не существует!"})

        queryset = AnswerPlayers.objects.filter(answer__isnull=False,
                                                        round_of_answer=current_round,
                                                        room=current_room)
        serializer = AnswerPlayersSerializer(queryset, many=True)
        return Response({'players': serializer.data})

    ########## result_room ##########
    # /game/result/
    @action(methods=['get'], detail=False, url_path='result')
    def vs_result_room(self, request):
        room_code = request.data.get('room_code')

        # проверка существует ли комната
        if not GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'massage': f"Комнаты {room_code} не существует!"})

        current_room = GameRoom.objects.get(room_code=room_code)
        current_round = GameRoom.objects.get(room_code=room_code).round
        queryset = AnswerPlayers.objects.filter(answer__isnull=False,
                                                round_of_answer=current_round,
                                                room=current_room)
        serializer = AnswerPlayersSerializer(queryset, many=True)
        return Response({'massage': serializer.data})

    ########## result_list_room ##########
    # /list
    @action(methods=['get'], detail=False, url_path='result/list')
    def vs_result_list_room(self, request):
        room_code = request.data.get('room_code')

        # проверка существует ли комната
        if not GameRoom.objects.filter(room_code=room_code).exists():
            return Response({'massage': f"Комнаты {room_code} не существует!"})

        current_room = GameRoom.objects.get(room_code=room_code)
        current_round = GameRoom.objects.get(room_code=room_code).round

        select = []
        for i in range(1, current_round + 1):
            question = Questions.objects.get(round_for_question=i)
            answer = AnswerPlayers.objects.filter(room=current_room, round_of_answer=i)
            one_obj = {"question": QuestionsSerializer(question, many=False).data,
                       "answers": AnswerPlayersSerializer(answer, many=True).data
                       }
            select.append(one_obj)

        return Response({'massage': select})


########## UNUSED ##########
class UNUSEDSet(RoomMixin, ModelViewSet):
    queryset = GameRoom.objects.all()
    serializer_class = GameRoomVueSerializer

    # /game/start/
    # TODO for what?
    @action(methods=['get'], detail=False, url_path='start')
    def vs_start_game(self, request):
        return Response({'massage': "vs_start_game"})

    # /game/start/
    # TODO for what?
    @action(methods=['get'], detail=False, url_path='room/waiting')
    def vs_waiting_room(self, request):
        return Response({'massage': "vs_waiting_room"})

    # /game/room/typing/
    @action(methods=['post'], detail=False, url_path='room/waiting/typing')
    def vs_waiting_typing_room(self, request):
        name_current_view_room = 'typing_room'
        room_code = request.data.get('room_code')
        return Response({'massage': "vs_waiting_typing_room"})
