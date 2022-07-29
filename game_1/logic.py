from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from game_1.models import GameRoom, Players

TEMP_CODE_ROOM = "SQPQ"
TEMP_NAME_USER = "Dima"
MAX_ROUNDS = 3

# class SupportFunction:
#
#     @classmethod
#     def is_room_exist(self, room_code=TEMP_CODE_ROOM):
#         """Существует ли комната"""
#
#         # https://django.fun/docs/django/ru/4.0/topics/http/shortcuts/
#         # try:
#         #     product = GameRoom.objects.get(room_code=room_code)
#         # except GameRoom.DoesNotExist:
#         #     raise Http404("Given query not found....")
#
#         if bool(GameRoom.objects.filter(room_code=room_code)):
#             return True
#         else:
#             massage = "(is_room_exist) Комната с кодом " + str(room_code) + " не существует!"
#             print(massage)
#             return None
#
#     @classmethod
#     def is_room_exist_exception(self, room_code=TEMP_CODE_ROOM):
#         pass
#
#     @classmethod
#     def get_current_room(self, room_code=TEMP_CODE_ROOM):
#         """Получить текущую комнату"""
#
#         if self.is_room_exist():
#             return GameRoom.objects.get(room_code=room_code)
#         else:
#             massage = "(get_current_room) Комнаты с кодом " + str(room_code) + " не существует!"
#             print(massage)
#             return None
#
#     @classmethod
#     def get_current_user(self, room_code=TEMP_CODE_ROOM):
#         """Получить текущего пользователя"""
#         pass
#
#     @classmethod
#     def is_user_in_room(self, user, room_code=TEMP_CODE_ROOM):
#         """Есть ли пользователь в комнате"""
#
#         if self.is_room_exist():
#             current_room = self.get_current_room()
#             players_room_in_room = current_room.players_set.filter(player_in_room=user)
#             return bool(players_room_in_room)
#         else:
#             massage = "(is_user_in_room) Пользователя " + str(user) + " нет в комнате + str(room_code)!"
#             print(massage)
#             return None
#
#     @classmethod
#     def is_user_in_room_exception(self, room_code=TEMP_CODE_ROOM):
#         pass
#
#     @classmethod
#     def delete_room(self, room_code=TEMP_CODE_ROOM):
#         """Удаляет игровую комнату с кодом комнаты"""
#
#         self.get_current_room().delete()
#         game_massage = "(delete_room) Была удалена комната с кодом " + str(room_code)
#         messages.success(self.request, game_massage)
#
#
#     @classmethod
#     def create_room(self, room_code=TEMP_CODE_ROOM):
#         """Создает игровую комнату с кодом комнаты"""
#
#         if self.is_room_exist():
#             massage = "Комната с кодом " + str(room_code) + " уже существует!"
#         else:
#             GameRoom.objects.create(room_code=room_code)
#             massage = "(create_room) Был создана комната с кодом " + str(room_code)
#
#         extra_context = {'massage': massage}
#
#         return extra_context
#
#     @classmethod
#     def start_game(self, room_code=TEMP_CODE_ROOM):
#         """Запускаем игру (меняем в БД статус)"""
#
#         if self.is_room_exist():
#             current_room = SupportFunction.get_current_room()
#             current_room.status_game = True
#             current_room.save()
#             massage = "(start_game) Игра запущена с кодом " + str(current_room)
#             extra_context = {'massage': massage}
#
#             return extra_context
#         else:
#             return None
#
#     def end_game(self):
#         """Завершаем игру (меняем в БД статус)"""
#
#         if self.is_room_exist():
#             current_room = SupportFunction.get_current_room()
#             current_room.status_game = False
#             current_room.save()
#             massage = "(start_game) Игра окончена с кодом комнаты" + str(current_room)
#             extra_context = {'massage': massage}
#
#             return extra_context
#         else:
#             return None
#
#     @classmethod
#     def next_round(self, room_code=TEMP_CODE_ROOM):
#         """Повышаем раунд игры (меняем в БД статус)"""
#
#         current_room = self.get_current_room()
#         current_room.round += 1
#         current_room.save()
#         massage = "(next_round) Раунд комнаты с кодом " + str(current_room) + " увеличен до " + str(
#             current_room.round)
#
#         return massage
#
#     @classmethod
#     def players_in_game(self, room_code=TEMP_CODE_ROOM):
#         """Выводит игроков в текущей игре с кодом комнаты"""
#
#         # Список игроков
#         players = self.get_current_room().players_set.all()
#
#         return players
#
#     @classmethod
#     def add_user_to_game(self, request):
#         """Добавить пользователя к комнате"""
#
#         current_user = request.user
#         current_game = self.get_current_room()
#         status_game = current_game.status_game
#         is_current_user_in_game = bool(current_game.players_set.filter(player_in_room=current_user))
#
#         if is_current_user_in_game:
#             massage = "(add_user_to_game) Пользователь " + current_user.username + " уже есть в игре " + TEMP_CODE_ROOM
#         # elif status_game:
#         #     massage = "(add_user_to_game) Игра закончена? - " + str(status_game)
#         else:
#             Players.objects.create(parent_room=current_game, player_in_room=current_user)
#             massage = "(add_user_to_game) Пользователь " + current_user.username + " был добавлен в игру " + TEMP_CODE_ROOM
#
#         extra_context = {'massage': massage}
#         return extra_context
#
#     @classmethod
#     def remove_user_to_game(self, request):
#         """Добавить пользователя к комнате"""
#
#         current_user = request.user
#         current_game = self.get_current_room()
#         status_game = current_game.status_game
#         is_current_user_in_game = bool(current_game.players_set.filter(player_in_room=current_user))
#
#         if not is_current_user_in_game:
#             massage = "(remove_user_to_game) Пользователь " + current_user.username + " нет в игре " + TEMP_CODE_ROOM
#         else:
#             Players.objects.get(parent_room=current_game, player_in_room=current_user).delete()
#             massage = "(remove_user_to_game) Пользователь " + current_user.username + " был удален из игры " + TEMP_CODE_ROOM
#
#         extra_context = {'massage': massage}
#         return extra_context
#
#     @classmethod
#     def delete_all_user_to_game(self, request, room_code=TEMP_CODE_ROOM):
#         """Удалить всх пользователй из игры c кодом"""
#
#         current_game = self.get_current_room()
#         players_in_current_game = current_game.players_set.all()
#
#         massage = "Было удалено " + str(len(players_in_current_game)) + " пользователей игры " + TEMP_CODE_ROOM
#         players_in_current_game.delete()
#
#         extra_context = {'massage': massage}
#         return extra_context

class RounMdixin:
    """Получим текущий раунд"""

    def get_current_round(self, room_code=TEMP_CODE_ROOM):
        """Получить текущий раунд"""
        if SupportFunction.is_room_exist():
            return SupportFunction.get_current_room().round

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['round'] = self.get_current_round()
        return context

class MassageMdixin:
    """Добавим переменную где хранятся мои сообщения"""

    def __init__(self, *args, **kwargs):
        # переменная класса для сообщений
        self._game_massage = []
        super().__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # добавдяем все что было в сообщений в context
        kwargs['game_massage'] = self._game_massage
        return super().get(request, *args, **kwargs)

class RoomMixin:

    def get_current_room(self, room_code=TEMP_CODE_ROOM):
        """Получить текущую комнату"""

        return GameRoom.objects.get(room_code=room_code)

    def delete_room(self, room_code=TEMP_CODE_ROOM):
        """Удаляет игровую комнату с кодом комнаты"""

        self.get_current_room().delete()
        game_massage = "(delete_room) Была удалена комната с кодом " + str(room_code)
        messages.success(self.request, game_massage)

    def create_room(self, room_code=TEMP_CODE_ROOM):
        """Создает игровую комнату с кодом комнаты"""

        if GameRoom.objects.filter(room_code=room_code):
            game_massage = "Комната с кодом " + str(room_code) + " уже существует!"
        else:
            GameRoom.objects.create(room_code=room_code)
            game_massage = "(create_room) Был создана комната с кодом " + str(room_code)
        messages.success(self.request, game_massage)

    def delete_all_users(self, request, room_code=TEMP_CODE_ROOM):
        """Удалить всх пользователй из игры c кодом"""

        current_game = self.get_current_room()
        players_in_current_game = current_game.players_set.all()

        game_massage = "Было удалено " + str(len(players_in_current_game)) + " пользователей игры " + TEMP_CODE_ROOM
        players_in_current_game.delete()
        messages.success(self.request, game_massage)

    def join_to_game(self, request):
        """Добавить пользователя к комнате"""

        current_user = self.request.user
        current_game = self.get_current_room()
        status_game = current_game.status_game
        is_current_user_in_game = bool(current_game.players_set.filter(player_in_room=current_user))

        if is_current_user_in_game:
            game_massage = "(add_user_to_game) Пользователь " + current_user.username + " уже есть в игре " + TEMP_CODE_ROOM
        # elif status_game:
        #     game_massage = "(add_user_to_game) Игра закончена? - " + str(status_game)
        else:
            Players.objects.create(parent_room=current_game, player_in_room=current_user)
            game_massage = "(add_user_to_game) Пользователь " + current_user.username + " был добавлен в игру " + TEMP_CODE_ROOM
        messages.success(self.request, game_massage)

    def exit_to_game(self, request):
        """Добавить пользователя к комнате"""

        current_user = self.request.user
        current_game = self.get_current_room()
        status_game = current_game.status_game
        is_current_user_in_game = bool(current_game.players_set.filter(player_in_room=current_user))

        if not is_current_user_in_game:
            game_massage = "(remove_user_to_game) Пользователь " + current_user.username + " нет в игре " + TEMP_CODE_ROOM
        else:
            Players.objects.get(parent_room=current_game, player_in_room=current_user).delete()
            game_massage = "(remove_user_to_game) Пользователь " + current_user.username + " был удален из игры " + TEMP_CODE_ROOM
        messages.success(self.request, game_massage)

    def start_game(self, room_code=TEMP_CODE_ROOM):
        """Запускаем игру (меняем в БД статус)"""

        current_room = self.get_current_room()
        current_room.status_game = True
        current_room.save()
        game_massage = "(start_game) Игра запущена с кодом " + str(current_room)
        messages.success(self.request, game_massage)

    def end_game(self):
        """Завершаем игру (меняем в БД статус)"""

        current_room = self.get_current_room()
        current_room.status_game = False
        current_room.save()
        game_massage = "(end_game) Статус игры с кодом комнаты " + str(current_room) + " изменен на " + str(current_room.status_game)
        messages.success(self.request, game_massage)

    def is_user_in_room(self, user, room_code=TEMP_CODE_ROOM):
        """Есть ли пользователь в комнате"""
        current_room = self.get_current_room()
        players_in_room = current_room.players_set.filter(player_in_room=user)
        if not players_in_room:
            game_massage = "(is_user_in_room) Пользователя " + str(user) + " нет в комнате " + str(room_code)
            messages.error(self.request, game_massage)
        return bool(players_in_room)

    def players_in_game(self, room_code=TEMP_CODE_ROOM):
        """Выводит игроков в текущей игре с кодом комнаты"""

        return self.get_current_room().players_set.all()


    def next_round(self, room_code=TEMP_CODE_ROOM):
        """Повышаем раунд игры (меняем в БД статус)"""

        current_room = self.get_current_room()
        current_room.round += 1
        current_room.save()
        game_massage = "(next_round) Раунд комнаты с кодом " + str(current_room) + " увеличен до " + str(current_room.round)
        messages.success(self.request, game_massage)