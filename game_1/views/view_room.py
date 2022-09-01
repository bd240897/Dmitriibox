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
        # kwargs['slug'] = 'SQPQ'
        kwargs['rules'] = Rules.objects.all()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form_room_code = form.cleaned_data.get("room_code")

        # if self.request.user.is_anonymous:
        #     # Если пользователь не вошел в систему
        #     game_massage = "Вы не залогинились в игру!"
        #     messages.error(self.request, game_massage)
        #     return HttpResponseRedirect(reverse("game_login"))

        # игра уже существует
        if GameRoom.objects.filter(room_code=form_room_code).exists():
            game_massage = "Комната " + str(form_room_code) + " уже существует!"
            messages.error(self.request, game_massage)
            # TODO редирект куда? уже на существующую игру
            # RejoinGameView
            # return HttpResponseRedirect(reverse("rejoin_game", kwargs={'slug': self.room_code}))
        # создадим игру (комнату)
        else:
            # создает новую игру status = 'main_room'
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
    name_current_view_room = 'waiting_room'

    @method_decorator(get_if_room_not_exist())
    def get(self, *args, **kwargs):

        # Игра status = 'waiting_room'
        self.switch_game_status(self.name_current_view_room)

        # параметры строки запроса
        param_request_delete_players = self.request.GET.get("deleteplayers", 0)
        param_request_delete_room = self.request.GET.get("deleteroom", 0)
        param_request_join = self.request.GET.get("join", 0)
        param_request_exit = self.request.GET.get("exit", 0)
        param_request_create = self.request.GET.get("create", 0)
        param_request_startgame = self.request.GET.get("startgame", 0)

        # удалить комнату
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

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user_in_room'] = self.current_room.is_user_in_room(self.request.user)
        context['is_user_owner'] = self.current_room.is_user_owner(self.request.user)
        context['players'] = self.players_in_game()
        return context




class StartGameView(RoomMixin, View):
    """Начинает игру (чисто редирект)"""

    def get(self, *args, **kwargs):

        # проверяем есть ли пользователь в комнате
        if self.is_user_in_room():
            game_massage = "Пользователь " + str(self.current_user) + " есть в комнате " + str(self.room_code)
            messages.success(self.request, game_massage)
            # TODO ЭТА ПРОВЕРКА НЕ НУЖНА Т,К, ДАМИН ПО УМОЛЧАНИЮ В КОМНАТЕ - эта проверка нужна для "присиоединитьсяк игре"


            return HttpResponseRedirect(reverse("typing_room", kwargs={'slug': self.room_code}))
        # TODO - а нужно ли проверять есть ли owner в комнате - мб сразу его добавить?
        else:
            game_massage = "Пользователя " + str(self.current_user) \
                           + " нет в комнате " + str(self.room_code)
            messages.error(self.request, game_massage)
            return HttpResponseRedirect(reverse("waiting_room", kwargs={'slug': self.room_code}))


class RejoinGameView(RoomMixin, View):
    pass
    # TODO

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
        self.switch_game_status(self.name_current_view_room)

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
        self.switch_game_status(self.name_current_view_room)

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
    name_current_view_room = 'result_room'

    @method_decorator(get_if_room_not_exist())
    def get(self, *args, **kwargs):

        # # TODO status = 'result_room'
        # # Игра status = 'waiting_typing_room'
        # self.switch_game_status('result_room')

        param_request_nextround = self.request.GET.get("nexround", 0)
        param_request_result_list = self.request.GET.get("result_list", 0)

        # смотрим все ответы
        if param_request_result_list:
            return HttpResponseRedirect(reverse("result_list_room", kwargs={'slug': self.room_code}))

        # TODO разобраться что делать если игра закончена - на экран конца или ответы
        # следующий раунд
        if param_request_nextround:
            # если вопросы кончились - переходим в "вспомним ответы"
            if self.is_questions_end():
                return HttpResponseRedirect(reverse("result_list_room", kwargs={'slug': self.room_code}))
            # следующий раунд
            else:
                self.next_round()
                self.switch_game_status('typing_room')
                return HttpResponseRedirect(reverse("typing_room", kwargs={'slug': self.room_code}))
        else:
            # простой заход в комнату - смотрим ответы раунды
            self.switch_game_status(self.name_current_view_room)

        return super().get(self, *args, **kwargs)

    def get_queryset(self):
        select = AnswerPlayers.objects.filter(answer__isnull=False,
                                              round_of_answer=self.current_round,
                                              room=self.current_room)
        return select

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
    name_current_view_room = "result_list_room"

    @method_decorator(get_if_room_not_exist())
    def get(self, request, *args, **kwargs):

        # Игра status = 'result_list_room'
        self.switch_game_status(self.name_current_view_room)

        param_request_end_game = self.request.GET.get("gameover", 0)

        # смотрим все ответы
        if param_request_end_game:
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
    name_current_view_room = "gameover_room"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_user_owner'] = self.current_room.is_user_owner(self.request.user)
        return context

    def get(self, request, *args, **kwargs):

        # Игра status = 'gameover_room'
        self.switch_game_status(self.name_current_view_room)

        # удалить игру
        param_request_delete = self.request.GET.get("delete", 0)
        if param_request_delete:
            self.delete_room()
            return redirect("main_room")
        return super().get(self, request, *args, **kwargs)

