from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from game_1.models import GameRoom, Players

TEMP_CODE_ROOM = "SQPQ"
TEMP_NAME_USER = "Dima"
MAX_ROUNDS = 3

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

        self.get_current_room(room_code=room_code).delete()
        game_massage = "(delete_room) Была удалена комната с кодом " + str(room_code)
        messages.success(self.request, game_massage)

    def create_room(self, room_code=TEMP_CODE_ROOM):
        """Создает игровую комнату с кодом комнаты"""

        if GameRoom.objects.filter(room_code=room_code):
            game_massage = "Комната с кодом " + str(room_code) + " уже существует!"
        else:
            GameRoom.objects.create(room_code=room_code, round=1)
            game_massage = "(create_room) Был создана комната с кодом " + str(room_code)
        messages.success(self.request, game_massage)

    def delete_all_users(self, room_code=TEMP_CODE_ROOM):
        """Удалить всх пользователй из игры c кодом"""

        current_game = self.get_current_room(room_code=room_code)
        room_code = current_game.room_codes
        players_in_current_game = current_game.players_set.all()

        game_massage = "Было удалено " + str(len(players_in_current_game)) + " пользователей игры " + str(room_code)
        players_in_current_game.delete()
        messages.success(self.request, game_massage)

    def join_to_game(self, room_code=TEMP_CODE_ROOM):
        """Добавить пользователя к комнате"""

        current_user = self.request.user
        current_game = self.get_current_room(room_code=room_code)
        room_code = current_game.room_code
        status_game = current_game.status_game
        is_current_user_in_game = bool(current_game.players_set.filter(player_in_room=current_user))

        if is_current_user_in_game:
            game_massage = "(add_user_to_game) Пользователь " + current_user.username + " уже есть в игре " + str(room_code)
            messages.error(self.request, game_massage)
        # elif status_game:
        #     game_massage = "(add_user_to_game) Игра закончена? - " + str(status_game)
        else:
            Players.objects.create(parent_room=current_game, player_in_room=current_user)
            game_massage = "(add_user_to_game) Пользователь " + current_user.username + " был добавлен в игру " + str(room_code)
            messages.success(self.request, game_massage)

    def exit_to_game(self, room_code=TEMP_CODE_ROOM):
        """Добавить пользователя к комнате"""

        current_user = self.request.user
        current_game = self.get_current_room(room_code=room_code)
        room_code = current_game.room_code
        status_game = current_game.status_game
        is_current_user_in_game = bool(current_game.players_set.filter(player_in_room=current_user))

        if not is_current_user_in_game:
            game_massage = "(remove_user_to_game) Пользователь " + current_user.username + " нет в игре " + str(room_code)
        else:
            Players.objects.get(parent_room=current_game, player_in_room=current_user).delete()
            game_massage = "(remove_user_to_game) Пользователь " + current_user.username + " был удален из игры " + str(room_code)
        messages.success(self.request, game_massage)

    def start_game(self, room_code=TEMP_CODE_ROOM):
        """Запускаем игру (меняем в БД статус)"""

        current_room = self.get_current_room(room_code=room_code)
        current_room.status_game = True
        current_room.save()
        game_massage = "(start_game) Статус игры с кодом комнаты " + str(current_room) + " изменен на " + str(current_room.status_game)
        messages.success(self.request, game_massage)

    def end_game(self, room_code=TEMP_CODE_ROOM):
        """Завершаем игру (меняем в БД статус)"""

        current_room = self.get_current_room(room_code=room_code)
        current_room.status_game = False
        current_room.save()
        game_massage = "(end_game) Статус игры с кодом комнаты " + str(current_room) + " изменен на " + str(current_room.status_game)
        messages.success(self.request, game_massage)

    def is_user_in_room(self, user, room_code=TEMP_CODE_ROOM):
        """Есть ли пользователь в комнате"""
        current_room = self.get_current_room(room_code=room_code)
        players_in_room = current_room.players_set.filter(player_in_room=user)
        if not players_in_room:
            game_massage = "(is_user_in_room) Пользователя " + str(user) + " нет в комнате " + str(room_code)
            messages.error(self.request, game_massage)
        return bool(players_in_room)

    def players_in_game(self, room_code=TEMP_CODE_ROOM):
        """Выводит игроков в текущей игре с кодом комнаты"""

        return self.get_current_room(room_code=room_code).players_set.all()


    def next_round(self, room_code=TEMP_CODE_ROOM):
        """Повышаем раунд игры (меняем в БД статус)"""

        current_room = self.get_current_room()
        current_room.round += 1
        current_room.save()
        game_massage = "(next_round) Раунд комнаты с кодом " + str(current_room) + " увеличен до " + str(current_room.round)
        messages.success(self.request, game_massage)