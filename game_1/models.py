from django.contrib.auth.models import User
from django.db import models



class GameRoom(models.Model):
    """Игровая комната"""

    room_code = models.CharField(max_length=4)
    create_time = models.DateTimeField(auto_now=True)
    # при создании игры None, при запуске True, при окончании False
    status_game = models.BooleanField(blank=True, null=True)
    round = models.IntegerField(blank=True, default=1)

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