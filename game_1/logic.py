from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from game_1.models import GameRoom

TEMP_CODE_ROOM = "SQPQ"
TEMP_NAME_USER = "Dima"
MAX_ROUNDS = 7

class RoomMixin:

    def setup(self, request, *args, **kwargs):
        """Сохраняем номер комнаты в класс"""

        # self.current_room self.current_round self.room_code self.current_user
        self.room_code = kwargs.get('slug')
        self.current_room = self.get_current_room(room_code=self.room_code)
        self.current_round = self.current_room.round
        self.current_user = request.user
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Записываем номер комнаты в контекст"""

        kwargs['slug'] = self.room_code
        kwargs['round'] = self.current_round
        return super().get_context_data(**kwargs)

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

        if GameRoom.objects.filter(room_code=room_code).exists(): # CHECK
            game_massage = "Комната с кодом " + str(room_code) + " уже существует!"
        else:
            GameRoom.objects.create(room_code=room_code, round=1)
            game_massage = "(create_room) Был создана комната с кодом " + str(room_code)
        messages.success(self.request, game_massage)



    def delete_all_users(self, room_code=TEMP_CODE_ROOM):
        """Удалить всх пользователй из игры c кодом"""

        # TODO повторы
        # current_game = self.get_current_room(room_code=room_code) #self.current_game
        # room_code = current_game.room_code
        players_in_current_room = self.current_room.players

        game_massage = "Было удалено " + str(len(players_in_current_room)) + " пользователей игры " + str(room_code)
        messages.success(self.request, game_massage)

        players_in_current_room.clear()


    def join_to_game(self, room_code=TEMP_CODE_ROOM):
        """Добавить пользователя к комнате"""

        # TODO повторы
        # current_user = self.request.user
        # current_game = self.get_current_room(room_code=room_code)
        # room_code = current_game.room_code
        is_current_user_in_game = self.current_room.players.filter(pk=self.current_user.pk).exists()
        
        # TODO разобраться со статусом игры
        # if status_game is None:
        #     pass
        # elif status_game is True:
        #     game_massage = "(add_user_to_game) Игра уже идет - " + str(status_game)
        # elif status_game is False:
        #     game_massage = "(add_user_to_game) Игра уже закончена - " + str(status_game)

        if is_current_user_in_game:
            game_massage = "(add_user_to_game) Пользователь " + self.current_user.username + " уже есть в игре " + str(room_code)
            messages.error(self.request, game_massage)
        else:
            self.current_room.players.add(self.current_user)
            game_massage = "(add_user_to_game) Пользователь " + self.current_user.username + " был добавлен в игру " + str(room_code)
            messages.success(self.request, game_massage)

    def exit_to_game(self, room_code=TEMP_CODE_ROOM):
        """Добавить пользователя к комнате"""

        # TODO повторы
        # current_user = self.request.user
        # current_game = self.get_current_room(room_code=room_code)
        # room_code = current_game.room_code
        # status_game = current_game.status_game
        is_current_user_in_game = self.current_room.players.filter(pk=self.current_user.pk).exists()

        if not is_current_user_in_game:
            game_massage = "(remove_user_to_game) Пользователь " + self.current_user.username + " нет в игре " + str(room_code)
        else:
            self.current_room.players.remove(self.current_user)
            game_massage = "(remove_user_to_game) Пользователь " + self.current_user.username + " был удален из игры " + str(room_code)
        messages.success(self.request, game_massage)

    def start_game(self, room_code=TEMP_CODE_ROOM):
        """Запускаем игру (меняем в БД статус)"""

        # current_room = self.get_current_room(room_code=room_code)
        self.current_room.status_game = True
        self.current_room.save()
        game_massage = "(start_game) Статус игры с кодом комнаты " + str(self.current_room) + " изменен на " + str(self.current_room.status_game)
        messages.success(self.request, game_massage)

    def end_game(self, room_code=TEMP_CODE_ROOM):
        """Завершаем игру (меняем в БД статус)"""

        # current_room = self.get_current_room(room_code=room_code)
        self.current_room.status_game = False
        self.current_room.save()
        game_massage = "(end_game) Статус игры с кодом комнаты " + str(self.current_room) + " изменен на " + str(self.current_room.status_game)
        messages.success(self.request, game_massage)

    def is_user_in_room(self, room_code=TEMP_CODE_ROOM):
        """Есть ли пользователь в комнате"""

        # TODO нужно ли передавать тут юзера
        # TODO повторы
        # current_room = self.get_current_room(room_code=room_code)
        is_current_user_in_game = self.current_room.players.filter(pk=self.current_user.pk).exists()
        if not is_current_user_in_game:
            game_massage = "(is_user_in_room) Пользователя " + str(self.current_user) + " нет в комнате " + str(self.room_code)
            messages.error(self.request, game_massage)
        return is_current_user_in_game

    def players_in_game(self, room_code=TEMP_CODE_ROOM):
        """Выводит игроков в текущей игре с кодом комнаты"""

        return self.current_room.players.all()


    def next_round(self, room_code=TEMP_CODE_ROOM):
        """Повышаем раунд игры (меняем в БД статус)"""

        # TODO замнеить на uodate
        self.current_room.round += 1
        self.current_room.save()
        game_massage = "(next_round) Раунд комнаты с кодом " + str(self.current_room) + " увеличен до " + str(self.current_round)
        messages.success(self.request, game_massage)


class RoomCodeMixin:
    def setup(self, request, *args, **kwargs):
        """Сохраняем номер комнаты в класс"""
        # self.current_room self.current_round self.room_code self.current_user
        self.room_code = kwargs.get('slug')
        self.current_room = self.get_current_room(room_code=self.room_code)
        self.current_round = self.current_room.round
        self.current_user = request.user


        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Записываем номер комнаты в контекст"""

        kwargs['slug'] = self.room_code
        kwargs['round'] = self.current_round

        return super().get_context_data(**kwargs)

