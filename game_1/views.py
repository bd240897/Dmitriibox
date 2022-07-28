from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegisterUserForm, LoginUserForm, AnswerForm
from .logic import *
from .models import AnswerPlayers


class RegisterUser(CreateView):
    """Регистрация"""

    form_class = RegisterUserForm
    template_name = 'game_1/register.html'
    success_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    """Логин"""

    form_class = LoginUserForm
    template_name = 'game_1/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

class TempView(TemplateView):
    """Заглушка"""

    template_name = 'game_1/home.html'

def logout_user(request):
    """Разлогиниться"""

    logout(request)
    return redirect('login')


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
            extra_context = delete_all_user_to_game(self.request)
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
        extra_context = {}

        param_request_delete_players = self.request.GET.get("deleteplayers", 0)
        param_request_delete_room = self.request.GET.get("deleteroom", 0)
        param_request_join = self.request.GET.get("join", 0)
        param_request_create = self.request.GET.get("create", 0)
        param_request_startgame = self.request.GET.get("startgame", 0)

        # создать комнату
        if param_request_create:
            extra_context = create_room()
        # удалить комнату
        elif param_request_delete_room:
            extra_context = delete_room()
            return render(self.request, self.template_name_main_room, extra_context)
        # удалить игроков
        elif param_request_delete_players:
            extra_context = delete_all_user_to_game(self.request)
        # присоединиться к комнате
        elif param_request_join:
            extra_context = add_user_to_game(self.request)
        # начать игру
        elif param_request_startgame:
            extra_context = start_game()
            user = self.request.user
            if not is_user_in_room(user):
                context = {"massage" : "Вы не вошли в эту игру!"}
                return render(self.request, self.template_name, context)
            return redirect("typing_room")

        players_context = players_in_game()

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

    def form_valid(self, form):
        current_user = self.request.user
        current_room = GameRoom.objects.get(room_code=TEMP_CODE_ROOM)
        current_player = current_room.players_set.filter(player_in_room=current_user).last()

        # MY EXCEPTION
        if not current_player:
            return HttpResponse('Список игроков наверное пуст - ' + str(current_player))

        AnswerPlayers.objects.create(player=current_player,
                                     answer=form.cleaned_data.get("answer"),
                                     round=1
                                     )

        return redirect('waiting_typing_room') #super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('waiting_typing_room')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        param_request_nextround = self.request.GET.get("nexround", 0)
        if param_request_nextround:
            extra_context = next_round()
        return context

class WaitingTypingRoomView(TemplateView):
    """Ждем всех игроков после typing"""

    template_name = 'game_1/room/waiting_typing_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['players'] = AnswerPlayers.objects.filter(answer__isnull=False).filter(player__parent_room__room_code=TEMP_CODE_ROOM, round=1)
        return context


class ResultRoomView(ListView):
    """Смотрим результаты"""

    template_name = 'game_1/room/result_room.html'
    context_object_name = 'players'

    def get_queryset(self):

        select = AnswerPlayers.objects.filter(answer__isnull=False).filter(player__parent_room__room_code=TEMP_CODE_ROOM, round=1)
        return select