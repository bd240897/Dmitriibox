from django.contrib.auth.models import User
from django.db import models
from django.contrib import messages
from django.core.validators import MinLengthValidator
from django.http import HttpResponseRedirect
from django.urls import reverse
from .channel_logic import send_to_channel_layer, close_socket


class GameRoom(models.Model):
    """Игровая комната"""

    room_code = models.CharField(verbose_name="Код комнаты", max_length=4, validators=[MinLengthValidator(4)])
    create_time = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    owner = models.ForeignKey(User, verbose_name="Создатель", on_delete=models.PROTECT, related_name='game_owner_vue')  # blank=True, null=True,
    # https://django.fun/docs/django/ru/3.1/topics/db/examples/many_to_many/
    players = models.ManyToManyField(User, verbose_name="Игрок", blank=True, related_name='game_players_vue')
    # при создании игры None, при запуске True, при окончании False
    round = models.IntegerField(verbose_name="Раунд", blank=True, default=1)

    CHOICES = {
        # ('main_room', 'Игра создана'), # Этот статус я не использую
        ('waiting_room', 'Игра создана'),
        ('typing_room', 'Печатаем ответы'),
        ('waiting_typing_room', 'Ждем ответы'),
        ('result_room', 'Смотрим ответы'),
        ('result_list_room', 'Вспомним все ответы'),
        ('gameover_room', 'Игра закончена'),
    }

    status = models.CharField(verbose_name="Статус игры", max_length=32, default="main_room", blank=True, choices=CHOICES)

    def join_to_game(self, request, user):
        """Добавить пользователя к комнате"""

        is_current_user_in_game = self.players.filter(pk=user.pk).exists()

        if is_current_user_in_game:
            game_massage = "(add_user_to_game) Пользователь " + user.username + " уже есть в игре " + str(
                self.room_code)
            messages.error(request, game_massage)
        else:
            self.players.add(user)
            game_massage = "(add_user_to_game) Пользователь " + user.username + " был добавлен в игру " + str(
                self.room_code)
            messages.success(request, game_massage)

    def exit_to_game(self, request, user):
        """Добавить пользователя к комнате"""

        is_current_user_in_game = self.players.filter(pk=user.pk).exists()
        if not is_current_user_in_game:
            game_massage = "(remove_user_to_game) Пользователя " + user.username + " нет в игре " + str(
                self.room_code)
            messages.error(request, game_massage)
        else:
            self.players.remove(user)
            game_massage = "(remove_user_to_game) Пользователь " + user.username + " был удален из игры " + str(
                self.room_code)
            messages.success(request, game_massage)

    def players_in_game(self):
        """Выводит игроков в текущей игре с кодом комнаты"""

        return self.players.all()

    def delete_all_users(self, request):
        """Удалить всх пользователй из игры c кодом"""

        game_massage = "Было удалено " + str(len(self.players.count())) + \
                       " пользователей игры " + str(self.room_code)
        messages.success(request, game_massage)
        self.players.clear()

    def next_round(self, request):
        """Повышаем раунд игры (меняем в БД статус)"""

        self.round += 1
        self.save()
        game_massage = "(next_round) Раунд комнаты с кодом " \
                       + str(self.room_code) \
                       + " увеличен до " + str(self.round)
        messages.success(request, game_massage)

    def switch_game_status(self, request, user, status):
        """Смена статуса игры"""

        ALLOWED_STATUS = [i[0] for i in GameRoom.CHOICES]
        if (self.is_user_owner(user) or user.is_superuser) and status in ALLOWED_STATUS:
            self.status = status
            self.save()
            game_massage = "(switch_game_status) Статус игры с кодом комнаты " \
                           + str(self.room_code) + " изменен на " \
                           + str(self.status)
            messages.success(request, game_massage)

            # отправим статус игры по channels
            send_to_channel_layer(room_code=self.room_code, msg=self.status)
        elif status not in ALLOWED_STATUS:
            game_massage = "(switch_game_status) Статуса " + str(status) \
                           + " не существует"
            messages.error(request, game_massage)

    # TODO my be unused
    def redirect_to_game_status(self, request):
        """Перенаправление по статусу комнаты"""
        game_massage = "(redirect_to_game_status) Перенаправление на  " + str(self.status)
        messages.success(request, game_massage)
        return HttpResponseRedirect(reverse(self.status, kwargs={'slug': self.room_code}))

    def is_user_in_room(self, user):
        """Проверка есть ли пользователь в комнате"""
        return self.players.filter(pk=user.pk).exists()

    def is_user_owner(self, user):
        """Проверка является ли пользователь владельцем"""
        return bool(self.owner == user)

    def __str__(self):
        return str(self.room_code)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
        ordering = ('owner', 'create_time', )


class AnswerPlayers(models.Model):
    """Ответы игроков по раундам"""

    # увеличивается каждый раунд
    player = models.ForeignKey(User, verbose_name="Игрок", on_delete=models.CASCADE, blank=True, null=True, related_name='answer_vue')
    answer = models.TextField(verbose_name="Ответ",)  # blank=True, null=False
    round_of_answer = models.IntegerField(verbose_name="Раунд ответа",)  # blank=True, default=1
    room = models.ForeignKey(GameRoom, verbose_name="Комната", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.player} AnswerPlayers"

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ('room', )


class Questions(models.Model):
    """Список вопросов"""

    # увеличивается каждый раунд
    question = models.TextField(verbose_name="Вопрос", blank=True, null=True)
    right_answer = models.TextField(verbose_name="Правильный ответ", blank=True, null=True)
    round_for_question = models.IntegerField(verbose_name="Раунд ответа", blank=True, default=1)
    author = models.CharField(verbose_name="Автор вопроса", max_length=16, default='Dmitrii')
    img = models.ImageField(verbose_name="Картинка", upload_to='images/game_1/questions', blank=True, null=True)

    def __str__(self):
        return f"{self.round_for_question} Questions"

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('round_for_question', )


class Rules(models.Model):
    number = models.IntegerField(verbose_name="Номер",)
    header = models.TextField(verbose_name="Название", blank=True, null=True)
    description = models.TextField(verbose_name="Текст", blank=True, null=True)
    img = models.ImageField(verbose_name="Картинка", upload_to='images/game_1/rules/', blank=True, null=True)

    def __str__(self):
        return f"{self.number} Rules"

    class Meta:
        verbose_name = 'Правило'
        verbose_name_plural = 'Правила'
        ordering = ('number', )