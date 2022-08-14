from django.contrib.auth.models import User
from django.db import models
from django.contrib import messages



class GameRoom(models.Model):
    """Игровая комната"""

    room_code = models.CharField(max_length=4)
    create_time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    # при создании игры None, при запуске True, при окончании False
    status_game = models.BooleanField(blank=True, null=True)
    round = models.IntegerField(blank=True, default=1)

    def is_user_in_room(self, user):
        # if self.players_set.filter(player_in_room=user):
        #     game_massage = "Пользователь " + user.username + " есть в комнате " + str(self.room_code)
        #     messages.success(self.request, game_massage)
        # else:
        #     game_massage = "Пользователя " + user.username + " нет в комнате " + str(self.room_code)
        #     messages.error(self.request, game_massage)

        return bool(self.players_set.filter(player_in_room=user))

    def is_user_owner(self, user):
        return bool(self.owner == user)

    def __str__(self):
        return str(self.room_code)


class Players(models.Model):
    """Игроки в игровой комнате"""

    parent_room = models.ForeignKey('GameRoom', on_delete=models.CASCADE, blank=True, null=True)
    player_in_room = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.player_in_room) + "_Players"

class AnswerPlayers(models.Model):
    """Ответы игроков по раундам"""

    # увеличивается каждый раунд
    player = models.ForeignKey('Players', on_delete=models.CASCADE, blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    round_of_answer = models.IntegerField(blank=True, default=1)

    def __str__(self):
        return str(self.player) + "_AnswerPlayers"


class Questions(models.Model):
    """Список вопросов"""

    # увеличивается каждый раунд
    question = models.TextField(blank=True, null=True)
    round_for_question = models.IntegerField(blank=True, default=1)
    author = models.CharField(max_length=16, default='Dmitrii')
    img = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return str(self.author) + "_Questions"

class Rules(models.Model):
    number = models.IntegerField()
    header = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='game_1/rules/', blank=True, null=True)

    def __str__(self):
        return str(self.number) + "Rules"