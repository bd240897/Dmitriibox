from django.contrib.auth.models import User
from django.db import models
from django.contrib import messages

# TODO формить красиво поля БД (имена, related_namd,)
# TODO добавить сортировку полей в модели по умолчанию

class GameRoom(models.Model):
    """Игровая комната"""

    room_code = models.CharField(max_length=4)
    create_time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name='game_owner')
    # https://django.fun/docs/django/ru/3.1/topics/db/examples/many_to_many/
    players = models.ManyToManyField(User, blank=True, related_name='game_players')
    # при создании игры None, при запуске True, при окончании False
    round = models.IntegerField(blank=True, default=1)

    # TODO стутусы waiting - мешает, gameover - нужен
    # создана - таймер-начала - печатаем - ждем - смотрим - следущий раунд(печатаем) ... - закончена - удалена
    CHOICES = {
        ('created', 'Игра создана'),
        ('start_timer', 'Таймер начала'),
        ('typing', 'Печатаем ответы'),
        ('waiting', 'Ждем ответы'),
        ('looking', 'Смотрим ответы'),
        ('resulting', 'Вспомним все ответы'),
        ('ended', 'Игра закончена'),
        ('deleted', 'Игра удалена'),
    }
    status = models.CharField(max_length=16, default="created", blank=True, choices=CHOICES)

    def is_user_in_room(self, user):
        return self.players.filter(pk=user.pk).exists()

    def is_user_owner(self, user):
        return bool(self.owner == user)

    def __str__(self):
        return str(self.room_code)

# TODO убрать множественное число из названия модели
class AnswerPlayers(models.Model):
    """Ответы игроков по раундам"""

    # увеличивается каждый раунд
    player = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='answer_player')
    answer = models.TextField(blank=True, null=True)
    round_of_answer = models.IntegerField(blank=True, default=1)
    room = models.ForeignKey(GameRoom, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.player) + "_AnswerPlayers"


# TODO убрать множественное число из названия модели
class Questions(models.Model):
    """Список вопросов"""

    # увеличивается каждый раунд
    question = models.TextField(blank=True, null=True)
    right_answer = models.TextField(blank=True, null=True)
    round_for_question = models.IntegerField(blank=True, default=1)
    author = models.CharField(max_length=16, default='Dmitrii')
    img = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return str(self.round_for_question) + "_Questions"

# TODO убрать множественное число из названия модели
class Rules(models.Model):
    number = models.IntegerField()
    header = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='game_1/rules/', blank=True, null=True)

    def __str__(self):
        return str(self.number) + "_Rules"
