import functools

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
        if self.is_game_exist():
            self.current_room = self.get_current_room()
            self.current_round = self.current_room.round
            self.current_room_status = self.current_room.status
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Записываем номер комнаты в контекст"""

        kwargs['slug'] = self.room_code
        kwargs['round'] = self.current_round
        kwargs['max_rounds'] = MAX_ROUNDS
        kwargs['owner'] = self.current_room.owner

        return super().get_context_data(**kwargs)

    def switch_game_status(self, status):
        """Смена статуса игры"""

        ALLOWED_STATUS = ['created', 'start_timer', 'typing', 'waiting', 'looking', 'ended', 'deleted', "resulting"]
        if (self.current_room.is_user_owner(self.current_user) or self.current_user.is_superuser) and status in ALLOWED_STATUS:
            self.current_room.status = status
            self.current_room.save()
            game_massage = "(switch_game_status) Статус игры с кодом комнаты " \
                           + str(self.current_room) + " изменен на " \
                           + str(self.current_room.status)
            messages.success(self.request, game_massage)
        elif status not in ALLOWED_STATUS:
            game_massage = "(switch_game_status) Статусу " + str(status) \
                           + " не существует"
            messages.error(self.request, game_massage)


    def is_game_exist(self):
        """Существует ли комната с игрой"""
        return GameRoom.objects.filter(room_code=self.room_code).exists()

    def is_user_in_room(self):
        """Есть ли пользователь в комнате"""
        return self.current_room.players.filter(pk=self.current_user.pk).exists()

    def get_current_room(self):
        """Получить текущую комнату"""
        return GameRoom.objects.get(room_code=self.room_code)

    def delete_room(self):
        """Удаляет игровую комнату с кодом комнаты"""
        if self.current_room.is_user_owner(self.current_user) or self.current_user.is_superuser:
            self.get_current_room().delete()
            game_massage = "(delete_room) Была удалена комната с кодом " + str(self.room_code)
            messages.success(self.request, game_massage)

    def create_room(self):
        """Создает игровую комнату с кодом комнаты"""

        if GameRoom.objects.filter(room_code=self.room_code).exists():  # CHECK
            game_massage = "(create_room) Комната с кодом " + str(self.room_code) + " уже существует!"
            messages.error(self.request, game_massage)
        else:
            GameRoom.objects.create(room_code=self.room_code, round=1)
            game_massage = "(create_room) Был создана комната с кодом " + str(self.room_code)
            messages.success(self.request, game_massage)

    def delete_all_users(self):
        """Удалить всх пользователй из игры c кодом"""
        # TODO API
        players_in_current_room = self.current_room.players
        game_massage = "Было удалено " + str(len(players_in_current_room)) + " пользователей игры " + str(
            self.room_code)
        messages.success(self.request, game_massage)
        players_in_current_room.clear()

    def join_to_game(self):
        """Добавить пользователя к комнате"""
        # TODO API
        is_current_user_in_game = self.current_room.players.filter(pk=self.current_user.pk).exists()

        if is_current_user_in_game:
            game_massage = "(add_user_to_game) Пользователь " + self.current_user.username + " уже есть в игре " + str(
                self.room_code)
            messages.error(self.request, game_massage)
        else:
            self.current_room.players.add(self.current_user)
            game_massage = "(add_user_to_game) Пользователь " + self.current_user.username + " был добавлен в игру " + str(
                self.room_code)
            messages.success(self.request, game_massage)

    def exit_to_game(self):
        """Добавить пользователя к комнате"""
        # TODO API
        is_current_user_in_game = self.current_room.players.filter(pk=self.current_user.pk).exists()
        if not is_current_user_in_game:
            game_massage = "(remove_user_to_game) Пользователя " + self.current_user.username + " нет в игре " + str(
                self.room_code)
            messages.error(self.request, game_massage)
        else:
            self.current_room.players.remove(self.current_user)
            game_massage = "(remove_user_to_game) Пользователь " + self.current_user.username + " был удален из игры " + str(
                self.room_code)
            messages.success(self.request, game_massage)

    # def start_game(self):
    #     """Запускаем игру (меняем в БД статус)"""
    #
    #     self.current_room.status = "typing"
    #     self.current_room.save()
    #     game_massage = "(start_game) Статус игры с кодом комнаты " \
    #                    + str(self.current_room) + " изменен на " \
    #                    + str(self.current_room.status)
    #     messages.success(self.request, game_massage)

    # def start_game_waiting(self):
    #     """Запускаем игру (меняем в БД статус)"""
    #
    #     self.current_room.status = "waiting"
    #     self.current_room.save()
    #     game_massage = "(start_game) Статус игры с кодом комнаты " \
    #                    + str(self.current_room) + " изменен на " \
    #                    + str(self.current_room.status)
    #     messages.success(self.request, game_massage)

    # def start_game_looking(self):
    #     """Запускаем игру (меняем в БД статус)"""
    #
    #     self.current_room.status = "looking"
    #     self.current_room.save()
    #     game_massage = "(start_game) Статус игры с кодом комнаты " \
    #                    + str(self.current_room) + " изменен на " \
    #                    + str(self.current_room.status)
    #     messages.success(self.request, game_massage)

    # def end_game(self):
    #     """Завершаем игру (меняем в БД статус)"""
    #
    #     self.current_room.status = "ended"
    #     self.current_room.save()
    #     game_massage = "(end_game) Статус игры с кодом комнаты " \
    #                    + str(self.current_room) \
    #                    + " изменен на " + str(self.current_room.status)
    #     messages.success(self.request, game_massage)

    def players_in_game(self):
        """Выводит игроков в текущей игре с кодом комнаты"""
        # TODO API
        return self.current_room.players.all()

    def next_round(self):
        """Повышаем раунд игры (меняем в БД статус)"""

        self.current_room.round += 1
        self.current_room.save()
        self.current_round += 1
        game_massage = "(next_round) Раунд комнаты с кодом " \
                       + str(self.current_room) \
                       + " увеличен до " + str(self.current_round)
        messages.success(self.request, game_massage)


# /////////////////////// ДЕКАРАТОРЫ /////////////////

def get_if_room_not_exist():
    """Если комнаты не существует"""
    # https://stackoverflow.com/questions/31633259/django-how-to-use-decorator-in-class-based-view-methods
    # https://habr.com/ru/post/137223/

    def decorator(func):
        def wrapper(request, *args, **kwargs):

            # Если пользователь не авторизован отправить его на регистрацию
            if not request.user.is_authenticated:
                return redirect("game_login")

            # Если игры не существует направить его не главную
            room_code = kwargs.get('slug')
            if not GameRoom.objects.filter(room_code=room_code).exists():
                game_massage = "(get) Игры " + str(room_code) + " не существует!"
                messages.error(request, game_massage)
                return redirect("main_room")

            return func(request, *args, **kwargs)
        return wrapper
    return decorator

