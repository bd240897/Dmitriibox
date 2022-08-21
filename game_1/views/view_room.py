from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, DetailView, RedirectView
from rest_framework.views import APIView

from ..forms import *
from ..logic import *
from ..models import *
from ..serializers import *


# ///////////////// КОМНАТЫ //////////////////////////

class RedirectMainRoomView(RedirectView):
    """Простой редирект на главную"""

    # https://ustimov.org/posts/11/
    def get_redirect_url(self):
        return reverse('main_room')

class MainRoomView(CreateView):
    form_class = CreateRoomForm
    template_name = 'game_1/room/main_room.html'

    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # ЗАГЛУШКА ДЛЯ РАБОТЫ ПАНЕЛИ АДМИНА (МОЕЙ РУКОПИСНОЙ)
        kwargs['slug'] = 'SQPQ'
        kwargs['rules'] = Rules.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form_room_code = form.cleaned_data.get("room_code")

        if self.request.user.is_anonymous:
            # Если пользователь не вошел в систему
            game_massage = "Вы не залогинились в игру!"
            messages.error(self.request, game_massage)
            return HttpResponseRedirect(reverse("game_login"))
        elif GameRoom.objects.filter(room_code=form_room_code).exists():
            game_massage = "Комната с кодом " + str(form_room_code) + " уже существует!"
            messages.error(self.request, game_massage)
        else:
            object = form.save(commit=False)
            object.owner = self.request.user
            object.save()
            game_massage = "(create_room) Был создана комната с кодом " + str(form_room_code)
            messages.success(self.request, game_massage)

        return HttpResponseRedirect(reverse("waiting_room", kwargs={'slug': form_room_code}))


class WaitingRoomTestView(RoomMixin, TemplateView):
    """Ожидание игроков"""

    # TODO выводить div с Игра уже идет. Игра еще не началась. и Кнопку начать игру убирать
    # TODO удаление комнаты сделать отдельным вью

    template_name = 'game_1/room/waiting_room_test.html'
    template_name_main_room = 'game_1/room/main_room.html'

    def get(self, *args, **kwargs):

        # Если пользователь не авторизован отправить его на регистрацию
        if not self.request.user.is_authenticated:
            return redirect("game_login")

        # параметры строки запроса
        param_request_delete_players = self.request.GET.get("deleteplayers", 0)
        param_request_delete_room = self.request.GET.get("deleteroom", 0)
        param_request_join = self.request.GET.get("join", 0)
        param_request_exit = self.request.GET.get("exit", 0)
        param_request_create = self.request.GET.get("create", 0)
        param_request_startgame = self.request.GET.get("startgame", 0)

        # создать комнату
        if param_request_create:
            self.create_room()
        # удалить комнату
        elif param_request_delete_room:
            self.delete_room()
            return redirect("main_room")
        # удалить игроков
        elif param_request_delete_players:
            self.delete_all_users()
        # присоединиться к комнате
        elif param_request_join:
            self.join_to_game()
        # выйти из комнаты
        elif param_request_exit:
            self.exit_to_game()
        # начать игру
        elif param_request_startgame:
            self.start_game()
            if not self.is_user_in_room():
                return super().get(*args, **kwargs)
            return HttpResponseRedirect(reverse("typing_room", kwargs={'slug': self.room_code}))

        kwargs['players'] = self.players_in_game()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user_in_room'] = self.current_room.is_user_in_room(self.request.user)
        context['is_user_owner'] = self.current_room.is_user_owner(self.request.user)
        return context


class WaitingRoomDeleteView(View):
    """Удалить пользователя из списка"""
    pass


class AddBotApiView(APIView):
    """Добавить бота в игру"""
    pass


class TypingRoomView(RoomMixin, CreateView):
    """Пишем ответы"""

    form_class = AnswerForm
    template_name = 'game_1/room/typing_room.html'

    def get(self, request, *args, **kwargs):

        # если игрок уже ответил на вопрос
        if AnswerPlayers.objects.filter(player=self.current_user, round_of_answer=self.current_round).exists():
            return HttpResponseRedirect(reverse("waiting_typing_room", kwargs={'slug': self.room_code}))

        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Получаем вопрос из БД"""

        # считывает форму и создает запись с ответом пользователя
        obj_question = get_object_or_404(Questions, round_for_question=self.current_round)
        kwargs['obj_question'] = obj_question

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # считывает форму и создает запись с ответом пользователя

        AnswerPlayers.objects.create(player=self.current_user,
                                     answer=form.cleaned_data.get("answer"),
                                     round_of_answer=self.current_round,
                                     room=self.current_room)

        return HttpResponseRedirect(reverse("waiting_typing_room", kwargs={'slug': self.room_code}))


class WaitingTypingRoomView(RoomMixin, TemplateView):
    """Ждем всех игроков после typing"""

    template_name = 'game_1/room/waiting_typing_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        already_answered = AnswerPlayers.objects.filter(answer__isnull=False,
                                                        round_of_answer=self.current_round,
                                                        room=self.current_room)
        players = [a.player for a in already_answered]
        context['players'] = players
        return context


class ResultRoomView(RoomMixin, ListView):
    """Смотрим результаты"""

    template_name = 'game_1/room/result_room.html'
    context_object_name = 'players'

    def get_queryset(self):
        select = AnswerPlayers.objects.filter(answer__isnull=False,
                                              round_of_answer=self.current_round,
                                              room=self.current_room)
        return select

    def get(self, *args, **kwargs):
        param_request_nextround = self.request.GET.get("nexround", 0)
        param_request_end_game = self.request.GET.get("gameover", 0)

        if param_request_end_game:
            self.end_game()
            self.delete_room()
            return redirect("gameover_room")
        if param_request_nextround:
            if self.is_questions_end():
                self.end_game()
                self.delete_room()
                return redirect("gameover_room")
            else:
                self.next_round()
                return HttpResponseRedirect(reverse("typing_room", kwargs={'slug': self.room_code}))

        return super().get(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Получаем вопрос из БД"""

        # https://django.fun/ru/cbv/Django/3.0/django.views.generic.list/ListView/
        # считывает форму и создает запись с ответом пользователя
        obj_question = get_object_or_404(Questions, round_for_question=self.current_round)
        kwargs['obj_question'] = obj_question

        return super().get_context_data(*args, **kwargs)

    def is_questions_end(self):
        return self.current_round >= MAX_ROUNDS


class GamveoverRoomView(TemplateView):
    """Страница спасибо за игру"""

    template_name = 'game_1/room/gameover_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ListResultsView(RoomMixin, ListView):
    """Показать список ответов"""
    model = AnswerPlayers
    template_name = 'game_1/room/list_result_room.html'
    context_object_name = 'obj_answer'

    def setup(self, request, *args, **kwargs):
        """Вызовем setup класса ListView"""

        self.room_code = kwargs.get('slug')
        self.current_user = request.user
        self.game_is_end = False
        # проверим есть ли комната, если нет то вызовем конструктор базового класса ListView а не RoomMixin
        if GameRoom.objects.filter(room_code=self.room_code).exists():
            self.current_room = self.get_current_room()
            self.current_round = self.current_room.round
        else:
            self.game_is_end = True
        super(ListView, self).setup(request, *args, **kwargs) # ListView.setup(self, request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.game_is_end:
            messages.error(self.request, '"Эта игра уже закончена и удалена')
            return redirect("main_room")
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        select = []
        for i in range(1, self.current_round):
            question = Questions.objects.get(round_for_question=i)
            print(question, 111)
            obj_answer = AnswerPlayers.objects.filter(room=self.current_room, round_of_answer=i)
            one_obj = {"question": question,
                       "answers": obj_answer
                       }
            select.append(one_obj)
        return select

    # qustion(round)
    # (user, answer)
    # a = {"qustion": "вопрос был",
    #      "round": 1,
    #      "obj_qustion": {"user": "amid", "answer": "11111"}
    #      }
    #
    # pass



