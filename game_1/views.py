from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .logic import *
from .models import *

class RegisterUser(CreateView):
    """Регистрация"""

    form_class = RegisterUserForm
    template_name = 'game_1/register.html'
    success_url = reverse_lazy('game_login')

    def get_success_url(self):
        return reverse_lazy('game_login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main_room')


class LoginUser(LoginView):
    """Логин"""

    form_class = LoginUserForm
    template_name = 'game_1/login.html'

    def get_success_url(self):
        return reverse_lazy('main_room')

class TempView(TemplateView):
    """Заглушка"""

    template_name = 'game_1/home.html'

def logout_user(request):
    """Разлогиниться"""

    logout(request)
    return redirect('main_room')


# КОМНАТЫ

class MainRoomView(TemplateView):
    """Главная страница игры"""

    template_name = 'game_1/room/main_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = dict()

        # параметр конца игры в запросе
        param_request_end_game = self.request.GET.get("gameover", 0)
        if param_request_end_game:
            extra_context = SupportFunction.delete_all_user_to_game(self.request)
            extra_context['gameover_massage'] = "Игра окончена"

        context = {**context, **extra_context}
        return context

class RedirectMainRoomView(View):
    """Простой редирект на главную"""

    def get(self, *args, **kwargs):
        return redirect("main_room")

class WaitingRoomView(View):
    """Ожидание игроков"""

    template_name = 'game_1/room/waiting_room.html'
    template_name_main_room = 'game_1/room/main_room.html'

    def get(self, *args, **kwargs):

        """Если пользователь не авторизован отправить его на регистрацию"""
        if not self.request.user.is_authenticated:
            return redirect("game_login")


        extra_context = {}

        param_request_delete_players = self.request.GET.get("deleteplayers", 0)
        param_request_delete_room = self.request.GET.get("deleteroom", 0)
        param_request_join = self.request.GET.get("join", 0)
        param_request_exit = self.request.GET.get("exit", 0)
        param_request_create = self.request.GET.get("create", 0)
        param_request_startgame = self.request.GET.get("startgame", 0)

        # создать комнату
        if param_request_create:
            extra_context = SupportFunction.create_room()
        # удалить комнату
        elif param_request_delete_room:
            extra_context = SupportFunction.delete_room()
            return render(self.request, self.template_name_main_room, extra_context)
        # удалить игроков
        elif param_request_delete_players:
            extra_context = SupportFunction.delete_all_user_to_game(self.request)
        # присоединиться к комнате
        elif param_request_join:
            extra_context = SupportFunction.add_user_to_game(self.request)
        # выйти из комнаты
        elif param_request_exit:
            extra_context = SupportFunction.remove_user_to_game(self.request)
        # начать игру
        elif param_request_startgame:
            extra_context = SupportFunction.start_game()
            user = self.request.user
            if not SupportFunction.is_user_in_room(user):
                context = {"massage" : "Вы не вошли в эту игру!"}
                return render(self.request, self.template_name, context)
            return redirect("typing_room")

        players_context = SupportFunction.players_in_game()

        context = {**players_context, **extra_context}
        return render(self.request, self.template_name, context)


# class WaitingRoomDeleteView(View):
#     """Удалить пользователя из списка"""
#
#     template_name = 'game_1/room/waiting_room.html'
#
#     def get(self, *args, **kwargs):
#         extra_context = delete_all_user_to_game(self.request)
#         players_context = players_in_game()
#         context = {**players_context, **extra_context}
#         return render(self.request, self.template_name, context)


class AddBotApiView(APIView):
    """Добавить бота в игру"""
    pass

class TypingRoomView(RounMdixin, CreateView):
    """Пишем ответы"""

    form_class = AnswerForm
    template_name = 'game_1/room/typing_room.html'

    # добавить проверку есть ли пользоватль в игре? и один ли он там!

    def create_answer(self, form):
        pass

    def get_context_data(self, **kwargs):
        """Получаем вопрос из БД"""

        # считывает форму и создает запись с ответом пользователя
        current_room = SupportFunction.get_current_room()
        current_round = current_room.round
        current_question = get_object_or_404(Questions, round_for_question=current_round).question
        kwargs['question'] = current_question

        return super().get_context_data(**kwargs)

    def form_valid(self, form):

        # считывает форму и создает запись с ответом пользователя
        current_user = self.request.user
        current_room = SupportFunction.get_current_room()
        current_player = current_room.players_set.filter(player_in_room=current_user).last()
        current_round = current_room.round

        # MY EXCEPTION
        if not current_player:
            return HttpResponse('Список игроков наверное пуст - ' + str(current_player))

        AnswerPlayers.objects.create(player=current_player,
                                     answer=form.cleaned_data.get("answer"),
                                     round_of_answer=current_round)

        return redirect('waiting_typing_room') #super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('waiting_typing_room')

class WaitingTypingRoomView(RounMdixin, TemplateView):
    """Ждем всех игроков после typing"""

    template_name = 'game_1/room/waiting_typing_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_round = SupportFunction.get_current_room().round
        context['players'] = AnswerPlayers.objects.filter(answer__isnull=False).filter(round_of_answer=current_round).filter(player__parent_room__room_code=TEMP_CODE_ROOM)
        return context


class ResultRoomView(RounMdixin, ListView):
    """Смотрим результаты"""

    template_name = 'game_1/room/result_room.html'
    context_object_name = 'players'

    def get_queryset(self):
        current_round = SupportFunction.get_current_room().round
        select = AnswerPlayers.objects.filter(answer__isnull=False).filter(round_of_answer=current_round).filter(player__parent_room__room_code=TEMP_CODE_ROOM,)
        return select

    def get(self, *args, **kwargs):
        param_request_nextround = self.request.GET.get("nexround", 0)

        if param_request_nextround:
            extra_context = SupportFunction.next_round()
            if self.is_questions_end():
                return redirect("gameover_room")
            else:
                return redirect("typing_room")

        return super().get(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Получаем вопрос из БД"""
        # https://django.fun/ru/cbv/Django/3.0/django.views.generic.list/ListView/
        current_room = SupportFunction.get_current_room()
        current_round = current_room.round

        # считывает форму и создает запись с ответом пользователя
        current_question = get_object_or_404(Questions, round_for_question=current_round).question
        kwargs['question'] = current_question

        return super().get_context_data(*args, **kwargs)

    def is_questions_end(self):
        current_room = SupportFunction.get_current_room()
        current_round = current_room.round
        return current_round > MAX_ROUNDS

class GamveoverRoomView(RounMdixin, TemplateView):
    """Страница спасибо за игру"""

    template_name = 'game_1/room/gameover_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class FindMethodsView(TemplateView):
    """Узнаем в каком порядке вызываютя методы"""
    """
    __init__
    setup
    dispatch
    get
    get_context_data
    render_to_response
    get_template_names
    """

    template_name = 'game_1/find_methods.html'

    def __init__(self, **kwargs):
        print("__init__")
        self.find_method = "I am here"
        super().__init__(**kwargs)

    def setup(self, request, *args, **kwargs):
        print("setup")
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        print("dispatch")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("get")
        kwargs['find_method'] = self.find_method
        return super().get(request, *args, **kwargs)

    # def get_queryset(self):
    #     print("get_queryset")
    #     return super().get_queryset()

    def get_context_data(self, **kwargs):
        print("get_context_data")
        return super().get_context_data(**kwargs)

    def get_template_names(self):
        print("get_template_names")
        return super().get_template_names()

    # def get_context_object_name(self, object_list):
    #     print("get_context_object_name")
    #     return super().get_context_object_name(object_list)

    def render_to_response(self, context, **response_kwargs):
        print("render_to_response")
        return super().render_to_response(context, **response_kwargs)

    # def as_view(cls, **initkwargs):
    #     print("as_view")
    #     return super().as_view(cls, **initkwargs)