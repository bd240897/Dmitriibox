from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
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
        kwargs['rules'] = Rules.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form_room_code = form.cleaned_data.get("room_code")

        # игра уже существует
        if GameRoom.objects.filter(room_code=form_room_code).exists():
            game_massage = "Комната " + str(form_room_code) + " уже существует!"
            messages.error(self.request, game_massage)
            # RejoinGameView
            return HttpResponseRedirect(reverse("rejoin_game", kwargs={'slug': form_room_code}))
        # создадим игру (комнату)
        else:
            # создает новую игру status = 'main_room'
            object = form.save(commit=False)
            object.owner = self.request.user
            object.save()
            # добавим сразу в комнату owners
            object.players.add(self.request.user)
            game_massage = "Был создана комната " + str(form_room_code)
            messages.success(self.request, game_massage)

        return HttpResponseRedirect(reverse("waiting_room", kwargs={'slug': form_room_code}))

class WaitingRoomTestView(RoomMixin, TemplateView):
    """Ожидание игроков"""
    # http://127.0.0.1:8000/room/waiting/SQPQ/

    # TODO выводить div с Игра уже идет. Игра еще не началась. и Кнопку начать игру убирать
    # TODO удаление комнаты сделать отдельным вью
    # TODO как переключаются раунды? админом комнаты?
    # TODO как заврешается игра? админом комнаты?

    template_name = 'game_1/room/waiting_room_test.html'
    template_name_main_room = 'game_1/room/main_room.html'
    name_current_view_room = 'waiting_room'

    @method_decorator(get_if_room_not_exist())
    def get(self, *args, **kwargs):

        # параметры строки запроса
        param_request_delete_players = self.request.GET.get("deleteplayers", 0)
        param_request_delete_room = self.request.GET.get("deleteroom", 0)
        param_request_join = self.request.GET.get("join", 0)
        param_request_exit = self.request.GET.get("exit", 0)
        param_request_startgame = self.request.GET.get("startgame", 0)

        # удалить комнату
        if param_request_delete_room:
            self.delete_room()
            return redirect("main_room")
        # удалить игроков
        elif param_request_delete_players:
            self.current_room.delete_all_users(self.request)
        # присоединиться к комнате
        elif param_request_join:
            self.current_room.join_to_game(self.request, self.current_user)
        # выйти из комнаты
        elif param_request_exit:
            self.current_room.exit_to_game(self.request, self.current_user)
        # начать игру
        elif param_request_startgame:
            return HttpResponseRedirect(reverse("typing_room", kwargs={'slug': self.room_code}))

        # Игра status = 'waiting_room'
        self.current_room.switch_game_status(self.request, self.current_user, self.name_current_view_room)

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user_in_room'] = self.current_room.is_user_in_room(self.request.user)
        context['is_user_owner'] = self.current_room.is_user_owner(self.request.user)
        context['players'] = self.current_room.players_in_game()
        context['room_code'] = self.room_code
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
    name_current_view_room = 'typing_room'

    @method_decorator(get_if_room_not_exist())
    def get(self, request, *args, **kwargs):

        # Игра status = 'typing_room'
        self.current_room.switch_game_status(self.request, self.current_user, self.name_current_view_room)

        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Получаем вопрос из БД"""

        # считывает форму и создает запись с ответом пользователя
        kwargs['obj_question'] = get_object_or_404(Questions, round_for_question=self.current_round)

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
    name_current_view_room = 'waiting_typing_room'

    @method_decorator(get_if_room_not_exist())
    def get(self, request, *args, **kwargs):

        # Игра status = 'waiting_typing_room'
        self.current_room.switch_game_status(self.request, self.current_user, self.name_current_view_room)

        return super().get(self, request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        already_answered = AnswerPlayers.objects.filter(answer__isnull=False,
                                                        round_of_answer=self.current_round,
                                                        room=self.current_room)
        context['players'] = [a.player for a in already_answered]
        context['is_user_owner'] = self.current_room.is_user_owner(self.request.user)
        return context


class ResultRoomView(RoomMixin, ListView):
    """Смотрим результаты раунда"""

    template_name = 'game_1/room/result_room.html'
    context_object_name = 'players'
    name_current_view_room = 'result_room'

    @method_decorator(get_if_room_not_exist())
    def get(self, *args, **kwargs):

        # вспомним все ответы
        param_request_result_list = self.request.GET.get("result_list", 0)
        if param_request_result_list:
            return HttpResponseRedirect(reverse("result_list_room", kwargs={'slug': self.room_code}))

        # следующий раунд
        param_request_nextround = self.request.GET.get("nexround", 0)
        if param_request_nextround:
            # если вопросы кончились - переходим в "вспомним ответы"
            if self.is_questions_end():
                return HttpResponseRedirect(reverse("result_list_room", kwargs={'slug': self.room_code}))
            # следующий раунд
            else:
                self.current_room.next_round(self.request)
                return HttpResponseRedirect(reverse("typing_room", kwargs={'slug': self.room_code}))

        # Игра status = 'waiting_typing_room'
        self.current_room.switch_game_status(self.request, self.current_user, self.name_current_view_room)

        return super().get(self, *args, **kwargs)

    def get_queryset(self):
        select = AnswerPlayers.objects.filter(answer__isnull=False,
                                              round_of_answer=self.current_round,
                                              room=self.current_room)
        return select

    def get_context_data(self, *args, **kwargs):
        """Получаем вопрос из БД"""

        # https://django.fun/ru/cbv/Django/3.0/django.views.generic.list/ListView/
        kwargs['obj_question'] = get_object_or_404(Questions, round_for_question=self.current_round)
        kwargs['is_user_owner'] = self.current_room.is_user_owner(self.request.user)
        return super().get_context_data(*args, **kwargs)

    def is_questions_end(self):
        return self.current_round >= MAX_ROUNDS


class ResultListView(RoomMixin, ListView):
    """Показать список ответов"""

    model = AnswerPlayers
    template_name = 'game_1/room/result_list_room.html'
    context_object_name = 'obj_answer'
    name_current_view_room = "result_list_room"

    @method_decorator(get_if_room_not_exist())
    def get(self, request, *args, **kwargs):

        # игра окончена
        param_request_end_game = self.request.GET.get("gameover", 0)
        if param_request_end_game:
            return HttpResponseRedirect(reverse("gameover_room", kwargs={'slug': self.room_code}))

        # продолжить игру
        param_request_continue = self.request.GET.get("continue", 0)
        if param_request_continue:
            return HttpResponseRedirect(reverse("result_room", kwargs={'slug': self.room_code}) + "?nexround=1")

        # Игра status = 'result_list_room'
        self.current_room.switch_game_status(self.request, self.current_user, self.name_current_view_room)

        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        # формироуем список ответов
        # TODO сделать красиво
        select = []
        for i in range(1, self.current_round+1):
            question = Questions.objects.get(round_for_question=i)
            obj_answer = AnswerPlayers.objects.filter(room=self.current_room, round_of_answer=i)
            one_obj = {"question": question,
                       "answers": obj_answer
                       }
            select.append(one_obj)
        return select


class GamveoverRoomView(RoomMixin, TemplateView):
    """Страница спасибо за игру"""

    template_name = 'game_1/room/gameover_room.html'
    name_current_view_room = "gameover_room"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user_owner'] = self.current_room.is_user_owner(self.request.user)
        return context

    def get(self, request, *args, **kwargs):

        # удалить игру
        param_request_delete = self.request.GET.get("delete", 0)
        if param_request_delete:
            self.delete_room()
            return redirect("main_room")

        # Игра status = 'gameover_room'
        self.current_room.switch_game_status(self.request, self.current_user, self.name_current_view_room)

        return super().get(self, request, *args, **kwargs)


class RejoinGameView(RoomMixin, View):
    """Возвращение в игру (чисто редирект)"""

    def get(self, *args, **kwargs):

        # если комната ожидания то можем присоединиться
        if self.current_room_status == 'waiting_room':
            return HttpResponseRedirect(reverse('waiting_room', kwargs={'slug': self.room_code}))
        # если пользователя нет в комнате
        elif not self.current_room.is_user_in_room(self.current_user):
            game_massage = "Игрока " + self.current_user.username + " нет в комнате " + str(self.current_room)
            messages.error(self.request, game_massage)
            return HttpResponseRedirect(reverse('main_room'))

        # если пользователь еще не ответил на вопрос
        current_room_status = self.current_room.status
        answer_exist = AnswerPlayers.objects.filter(room__room_code=self.current_room,
                                                    round_of_answer=self.current_round,
                                                    player=self.current_user).exists()

        if current_room_status == 'waiting_typing_room' and not answer_exist:
            game_massage = "Вы вернулись в игру " + str(self.current_room) + "со статусом " + str(current_room_status)
            messages.success(self.request, game_massage)
            return HttpResponseRedirect(reverse('typing_room', kwargs={'slug': self.room_code}))

        # просто попытка вернуться в комнату
        game_massage = "Вы вернулись в игру " + str(self.current_room) + "со статусом " + str(current_room_status)
        messages.success(self.request, game_massage)
        return HttpResponseRedirect(reverse(current_room_status, kwargs={'slug': self.room_code}))
