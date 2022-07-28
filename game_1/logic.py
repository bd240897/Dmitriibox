from django.contrib.auth.models import User
from django.http import HttpResponse

from game_1.models import GameRoom, Players

TEMP_CODE_ROOM = "SQPQ"
TEMP_NAME_USER = "Dima"


def create_room(room_code=TEMP_CODE_ROOM):
    """Создает игровую комнату с кодом комнаты"""
    extra_context = dict()

    if GameRoom.objects.filter(room_code=room_code):
        massage = "Комната с кодом " + str(room_code) + " уже существует!"
    else:
        GameRoom.objects.create(room_code=room_code)
        massage = "(create_room) Был создана комната с кодом " + str(room_code)
    extra_context['massage'] = massage

    return extra_context

def start_game(room_code=TEMP_CODE_ROOM):
    """Запускаем игру (меняем в БДЩ= статус)"""

    extra_context = dict()

    if GameRoom.objects.filter(room_code=room_code):
        massage = "(start_game) Комната с кодом " + str(room_code) + " не уже существует!"
        return HttpResponse(massage)
    else:
        current_room = GameRoom.objects.get(room_code=room_code)
        current_room.status_game = True
        current_room.save()
        massage = "(start_game) Игра запущена с кодом " + str(current_room)
        extra_context['massage'] = massage

        return extra_context

def delete_room(room_code=TEMP_CODE_ROOM):
    """Удаляет игровую комнату с кодом комнаты"""
    extra_context = dict()

    GameRoom.objects.get(room_code=room_code).delete()
    massage = "(delete_room) Была удалена комната с кодом " + str(room_code)
    extra_context['massage'] = massage

    return extra_context

def players_in_game(room_code=TEMP_CODE_ROOM):
    """Выводит игроков в текущей игре с кодом комнаты"""
    extra_context = dict()

    # Список игроков
    players = GameRoom.objects.get(room_code=room_code).players_set.all()
    extra_context["players"] = players

    # # Сообщение
    # players_in_game_list = [player.player_in_room.username for player in players]
    # massage = "(players_in_game) Был возвращен список игроков " + " ".join(players_in_game_list)
    # extra_context['massage'] = massage

    return extra_context


def add_user_to_game(request):
    """Добавить пользователя к комнате"""

    extra_context = dict()

    current_user = request.user
    current_game = GameRoom.objects.get(room_code=TEMP_CODE_ROOM)

    status_game = current_game.status_game
    is_current_user_in_game = bool(current_game.players_set.filter(player_in_room=current_user))

    if is_current_user_in_game and not status_game:
        massage = "(add_user_to_game) Пользователь " + current_user.username + " уже есть в игре " + TEMP_CODE_ROOM
    elif status_game:
        massage = "(add_user_to_game) Игра закончена? - " + str(status_game)
    else:
        Players.objects.create(parent_room=current_game, player_in_room=current_user)
        massage = "(add_user_to_game) Пользователь " + current_user.username + " был добавлен в игру " + TEMP_CODE_ROOM
    print(massage)

    extra_context['massage'] = massage
    return extra_context


def delete_all_user_to_game(request, room_code=TEMP_CODE_ROOM):
    """Удалить всх пользователй из игры c кодом"""

    context = dict()
    current_game = GameRoom.objects.get(room_code=room_code)
    players_in_current_game = current_game.players_set.all()

    temp_str = "Было удалено " + str(len(players_in_current_game)) + " пользователей игры " + TEMP_CODE_ROOM
    players_in_current_game.delete()

    context['massage'] = temp_str
    return context
