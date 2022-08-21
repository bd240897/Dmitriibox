from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import redirect

from game_1.models import GameRoom

TEMP_CODE_ROOM = "SQPQ"
TEMP_NAME_USER = "Dima"
MAX_ROUNDS = 7

class RoomMixin:

    def setup(self, request, *args, **kwargs):
        """Сохраняем номер комнаты в класс"""

        # self.current_room self.current_round self.room_code self.current_user
        self.room_code = kwargs.get('slug')
        self.current_user = request.user
        self.current_room = self.get_current_room()
        self.current_round = self.current_room.round
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Записываем номер комнаты в контекст"""

        kwargs['slug'] = self.room_code
        kwargs['round'] = self.current_round
        return super().get_context_data(**kwargs)

    def is_game_end(self, room_code):
        return GameRoom.objects.filter(room_code=room_code).exists()

    def get_current_room(self):
        """Получить текущую комнату"""

        return GameRoom.objects.get(room_code=self.room_code)

    def delete_room(self):
        """Удаляет игровую комнату с кодом комнаты"""

        self.get_current_room().delete()
        game_massage = "(delete_room) Была удалена комната с кодом " + str(self.room_code)
        messages.success(self.request, game_massage)

    def create_room(self):
        """Создает игровую комнату с кодом комнаты"""

        if GameRoom.objects.filter(room_code=self.room_code).exists(): # CHECK
            game_massage = "Комната с кодом " + str(self.room_code) + " уже существует!"
            messages.error(self.request, game_massage)
        else:
            GameRoom.objects.create(room_code=self.room_code, round=1)
            game_massage = "(create_room) Был создана комната с кодом " + str(self.room_code)
            messages.success(self.request, game_massage)


    def delete_all_users(self):
        """Удалить всх пользователй из игры c кодом"""

        players_in_current_room = self.current_room.players
        game_massage = "Было удалено " + str(len(players_in_current_room)) + " пользователей игры " + str(self.room_code)
        messages.success(self.request, game_massage)
        players_in_current_room.clear()


    def join_to_game(self):
        """Добавить пользователя к комнате"""

        is_current_user_in_game = self.current_room.players.filter(pk=self.current_user.pk).exists()
        
        # TODO разобраться со статусом игры
        # if status_game is None:
        #     pass
        # elif status_game is True:
        #     game_massage = "(add_user_to_game) Игра уже идет - " + str(status_game)
        # elif status_game is False:
        #     game_massage = "(add_user_to_game) Игра уже закончена - " + str(status_game)

        if is_current_user_in_game:
            game_massage = "(add_user_to_game) Пользователь " + self.current_user.username + " уже есть в игре " + str(self.room_code)
            messages.error(self.request, game_massage)
        else:
            self.current_room.players.add(self.current_user)
            game_massage = "(add_user_to_game) Пользователь " + self.current_user.username + " был добавлен в игру " + str(self.room_code)
            messages.success(self.request, game_massage)

    def exit_to_game(self):
        """Добавить пользователя к комнате"""

        is_current_user_in_game = self.current_room.players.filter(pk=self.current_user.pk).exists()
        if not is_current_user_in_game:
            game_massage = "(remove_user_to_game) Пользователя " + self.current_user.username + " нет в игре " + str(self.room_code)
            messages.error(self.request, game_massage)
        else:
            self.current_room.players.remove(self.current_user)
            game_massage = "(remove_user_to_game) Пользователь " + self.current_user.username + " был удален из игры " + str(self.room_code)
            messages.success(self.request, game_massage)

    def start_game(self):
        """Запускаем игру (меняем в БД статус)"""

        # TODO заменить на update
        self.current_room.status_game = True
        self.current_room.save()
        game_massage = "(start_game) Статус игры с кодом комнаты " + str(self.current_room) + " изменен на " + str(self.current_room.status_game)
        # TODO со статусом игры - если агру уже закончена
        messages.success(self.request, game_massage)

    def end_game(self):
        """Завершаем игру (меняем в БД статус)"""

        # TODO заменить на update
        self.current_room.status_game = False
        self.current_room.save()
        game_massage = "(end_game) Статус игры с кодом комнаты " + str(self.current_room) + " изменен на " + str(self.current_room.status_game)
        # TODO со статусом игры - если агру уже закончена
        messages.success(self.request, game_massage)

    def is_user_in_room(self):
        """Есть ли пользователь в комнате"""

        is_current_user_in_game = self.current_room.players.filter(pk=self.current_user.pk).exists()
        if not is_current_user_in_game:
            game_massage = "(is_user_in_room) Пользователя " + str(self.current_user) + " нет в комнате " + str(self.room_code)
            messages.error(self.request, game_massage)
        return is_current_user_in_game

    def players_in_game(self):
        """Выводит игроков в текущей игре с кодом комнаты"""

        return self.current_room.players.all()


    def next_round(self):
        """Повышаем раунд игры (меняем в БД статус)"""

        # TODO замнеить на uodate
        self.current_room.round += 1
        self.current_room.save()
        game_massage = "(next_round) Раунд комнаты с кодом " + str(self.current_room) + " увеличен до " + str(self.current_round)
        messages.success(self.request, game_massage)
