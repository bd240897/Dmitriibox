from django.contrib.auth.models import User

from game_1.models import GameRoom, Players

TEMP_CODE_ROOM = "SQPQ"
TEMP_NAME_USER = "Dima"

def players_in_game():
    players = GameRoom.objects.get(room_code=TEMP_CODE_ROOM).players_set.all()
    print("players - ", players)
    return {"players" : players}

def add_user_to_game(request):
    """Добавить пользователя к комнате"""

    context = dict()

    current_user = request.user
    print("current_user - ", current_user.username)
    current_game = GameRoom.objects.get(room_code=TEMP_CODE_ROOM)
    print("current_game - ", current_game)
    is_game_end = current_game.is_end
    print("is_game_end - ", is_game_end)
    is_current_user_in_game = current_game.players_set.filter(player=current_user)
    print("is_current_user_in_game - ", is_current_user_in_game)
    print("bool - ", bool(is_current_user_in_game))

    if is_current_user_in_game and not is_game_end:
        temp_str = "Пользователь " + current_user.username + " уже есть в игре " + TEMP_CODE_ROOM
        print(temp_str)
    elif is_game_end:
        temp_str = "Игра закончена? - " + str(is_game_end)
        print(temp_str)
    else:
        Players.objects.create(parent_room=current_game, player=current_user, round=1)
        temp_str = "Пользователь " + current_user.username + " был добавлен в игру " + TEMP_CODE_ROOM
        print(temp_str)

    context['massage'] = temp_str

    return context

def delete_all_user_to_game(request):
    """Удалить пользователй из игры"""

    context = dict()
    current_user = request.user
    current_game = GameRoom.objects.get(room_code=TEMP_CODE_ROOM)
    is_current_user_in_game = current_game.players_set.filter(player=current_user)

    if True:
        temp_str = "Было удалено " + str(len(is_current_user_in_game)) + " пользователей игры " + TEMP_CODE_ROOM
        is_current_user_in_game.delete()
        print(temp_str)

    context['massage'] = temp_str

    return context