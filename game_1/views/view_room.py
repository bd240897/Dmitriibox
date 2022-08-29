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
            game_massage = "Комната " + str(form_room_code) + " уже существует!"
            messages.error(self.request, game_massage)
        else:
            object = form.save(commit=False)
            object.owner = self.request.user
            object.save()
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

    @method_decorator(get_if_room_not_exist())
    def get(self, *args, **kwargs):

        # параметры строки запроса
        param_request_delete_players = self.request.GET.get("deleteplayers", 0)
        param_request_delete_room = self.request.GET.get("deleteroom", 0)
        param_request_join = self.request.GET.get("join", 0)
        param_request_exit = self.request.GET.get("exit", 0)
        param_request_create = self.request.GET.get("create", 0)
        param_request_startgame = self.request.GET.get("startgame", 0)

        # создать комнату если ее нет
        if param_request_create:
            self.create_room()

        # проверить статус комнаты
        if self.current_room_status == 'created':
            if param_request_delete_room:
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
                return HttpResponseRedirect(reverse("start_game", kwargs={'slug': self.room_code}))
        else:
            # попытка вернутся в игру
            return HttpResponseRedirect(reverse("rejoin_game", kwargs={'slug': self.room_code}))

        kwargs['players'] = self.players_in_game()
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user_in_room'] = self.current_room.is_user_in_room(self.request.user)
        context['is_user_owner'] = self.current_room.is_user_owner(self.request.user)
        return context


class StartGameView(RoomMixin, View):
    """Начинает игру (чисто редирект)"""

    def get(self, *args, **kwargs):
        # проверяем есть ли пользователь в комнате
        if self.is_user_in_room():
            game_massage = "Пользователь " + str(self.current_user) + " есть в комнате " + str(self.room_code)
            messages.success(self.request, game_massage)
            self.switch_game_status('typing')
            return HttpResponseRedirect(reverse("typing_room", kwargs={'slug': self.room_code}))
        else:
            game_massage = "Пользователя " + str(self.current_user) \
                           + " нет в комнате " + str(self.room_code)
            messages.error(self.request, game_massage)
            return HttpResponseRedirect(reverse("waiting_room", kwargs={'slug': self.room_code}))


class RejoinGameView(RoomMixin, View):
    """Возвращение в игру (чисто редирект)"""

    def get(self, *args, **kwargs):

        # возвращение в игру
        if self.current_room_status in ['typing', 'waiting', 'looking'] and self.is_user_in_room():
            game_massage = "Вы вернулись в игру " + str(self.current_room)
            messages.success(self.request, game_massage)

            # если пользователь дал ответ на этот раунд
            # TODO check
            if AnswerPlayers.objects.filter(room__room_code=self.current_room,
                                            round_of_answer=self.current_round,
                                            player=self.current_user).exists():
                game_massage = "Вы уже дали ответ в этом раунде " + str(self.current_room)
                messages.success(self.request, game_massage)
                return HttpResponseRedirect(reverse("waiting_typing_room", kwargs={'slug': self.room_code}))
            # если пользователь еще не дал ответ на этот раунд
            else:
                game_massage = "Вы еще на дали ответ в этом раунде " + str(self.current_room)
                messages.error(self.request, game_massage)
                return HttpResponseRedirect(reverse("typing_room", kwargs={'slug': self.room_code}))
        # игра уже идет или закончен и вас в ней нет
        else:
            game_massage = "Вернуться в игру" + str(self.current_room) \
                           + " не удалось, статус игры " + str(self.current_room.status) \
                           + " или вас нет в этой комнате"
            messages.error(self.request, game_massage)
            return redirect("main_room")


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

    @method_decorator(get_if_room_not_exist())
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
        self.switch_game_status('waiting')
        return HttpResponseRedirect(reverse("waiting_typing_room", kwargs={'slug': self.room_code}))


class WaitingTypingRoomView(RoomMixin, TemplateView):
    """Ждем всех игроков после typing"""

    template_name = 'game_1/room/waiting_typing_room.html'

    @method_decorator(get_if_room_not_exist())
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        already_answered = AnswerPlayers.objects.filter(answer__isnull=False,
                                                        round_of_answer=self.current_round,
                                                        room=self.current_room)
        players = [a.player for a in already_answered]
        context['players'] = players
        context['is_user_owner'] = self.current_room.is_user_owner(self.request.user)
        return context


class ResultRoomView(RoomMixin, ListView):
    """Смотрим результаты раунда"""

    template_name = 'game_1/room/result_room.html'
    context_object_name = 'players'

    def get_queryset(self):
        select = AnswerPlayers.objects.filter(answer__isnull=False,
                                              round_of_answer=self.current_round,
                                              room=self.current_room)
        return select

    @method_decorator(get_if_room_not_exist())
    def get(self, *args, **kwargs):

        param_request_nextround = self.request.GET.get("nexround", 0)
        param_request_result_list = self.request.GET.get("result_list", 0)

        # смотрим все ответы
        if param_request_result_list:
            self.switch_game_status("resulting")
            print("resulting")
            return HttpResponseRedirect(reverse("result_list_room", kwargs={'slug': self.room_code}))

        # TODO разобраться что делать если игра закончена - на экран конца или ответы
        # следующий раунд
        if param_request_nextround:
            # если вопросы кончились - переходим в "вспомним ответы"
            if self.is_questions_end():
                self.switch_game_status("resulting")
                return HttpResponseRedirect(reverse("result_list_room", kwargs={'slug': self.room_code}))
            # следующий раунд
            else:
                self.next_round()
                self.switch_game_status('typing')
                return HttpResponseRedirect(reverse("typing_room", kwargs={'slug': self.room_code}))
        else:
            # простой заход в комнату - смотрим ответы раунды
            self.switch_game_status('looking')

        return super().get(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Получаем вопрос из БД"""

        # https://django.fun/ru/cbv/Django/3.0/django.views.generic.list/ListView/
        obj_question = get_object_or_404(Questions, round_for_question=self.current_round)
        kwargs['obj_question'] = obj_question
        kwargs['is_user_owner'] = self.current_room.is_user_owner(self.request.user)
        return super().get_context_data(*args, **kwargs)

    def is_questions_end(self):
        return self.current_round >= MAX_ROUNDS


class ResultListView(RoomMixin, ListView):
    """Показать список ответов"""

    model = AnswerPlayers
    template_name = 'game_1/room/result_list_room.html'
    context_object_name = 'obj_answer'

    @method_decorator(get_if_room_not_exist())
    def get(self, request, *args, **kwargs):
        param_request_end_game = self.request.GET.get("gameover", 0)

        # смотрим все ответы
        if param_request_end_game:
            self.switch_game_status("ended")
            # TODO добавил slug к gameover, нужен ли он ему?
            return HttpResponseRedirect(reverse("gameover_room", kwargs={'slug': self.room_code}))
        return super().get(self, request, *args, **kwargs)

    def get_queryset(self):
        # формироуем список ответов
        # TODO сделать красиво
        select = []
        for i in range(1, self.current_round+1):
            question = Questions.objects.get(round_for_question=i)
            print(question, 111)
            obj_answer = AnswerPlayers.objects.filter(room=self.current_room, round_of_answer=i)
            one_obj = {"question": question,
                       "answers": obj_answer
                       }
            select.append(one_obj)
        return select


class GamveoverRoomView(RoomMixin, TemplateView):
    """Страница спасибо за игру"""

    template_name = 'game_1/room/gameover_room.html'

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
        return super().get(self, request, *args, **kwargs)