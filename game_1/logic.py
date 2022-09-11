import functools

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

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
        if self.is_room_exist():
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

    def is_room_exist(self):
        """Существует ли комната с игрой"""
        return GameRoom.objects.filter(room_code=self.room_code).exists()

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


# /////////////////////// ДЕКАРАТОРЫ /////////////////

def get_if_room_not_exist():
    """Если комнаты не существует"""
    # https://stackoverflow.com/questions/31633259/django-how-to-use-decorator-in-class-based-view-methods
    # https://habr.com/ru/post/137223/

    def decorator(func):
        def wrapper(request, *args, **kwargs):

            # Если пользователь не авторизован отправить его на регистрацию
            if not request.user.is_authenticated:
                game_massage = "Вы не залогинились в игру!"
                messages.error(request, game_massage)
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



