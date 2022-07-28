from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RegisterUserForm, LoginUserForm, AnswerForm
from .logic import *


class TestApiView(APIView):
    def get(self, request):
        return Response({"dima":"I am groud", 'masha':'I am a girl'})

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
        param_request_end_game = self.request.GET.get("gameover", 0)
        if param_request_end_game:
            extra_context = delete_all_user_to_game(self.request)
            extra_context['gameover_massage'] = "Игра окончена"

        context = {**context, **extra_context}
        return context


class WaitingRoomView(View):
    """Ожидание игроков"""

    template_name = 'game_1/room/waiting_room.html'

    def get(self, *args, **kwargs):
        extra_context = {}

        param_request_delete = self.request.GET.get("delete", 0)
        param_request_join = self.request.GET.get("join", 0)

        if param_request_delete:
            extra_context = delete_all_user_to_game(self.request)
        elif param_request_join:
            extra_context = add_user_to_game(self.request)

        players_context = players_in_game()

        context = {**players_context, **extra_context}
        return render(self.request, self.template_name, context)


class AddBotApiView(APIView):
    """Добавить бота в игру"""
    pass

class TypingRoomView(CreateView):
    """Пишем ответы"""

    model = GameRoom
    form_class = AnswerForm
    template_name = 'game_1/room/typing_room.html'

    # добавить проверку есть ли пользоватль в игре? и один ли он там!

    def form_valid(self, form):
        parent_room = GameRoom.objects.get(room_code=TEMP_CODE_ROOM)
        player = self.request.user
        # round

        # # костыль костыль!!!!!
        current_player = GameRoom.objects.get(room_code=TEMP_CODE_ROOM).players_set.last()
        current_player.round = 1
        current_player.answer = form.cleaned_data.get("answer")
        current_player.parent_room = parent_room
        current_player.save()

        # form.instance.parent_room = parent_room
        # form.instance.player = player
        # form.instance.a = player

        return redirect('waiting_typing_room') #super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('waiting_typing_room')


class WaitingTypingRoomView(TemplateView):
    """Ждем всех игроков после typing"""

    template_name = 'game_1/room/waiting_typing_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = GameRoom.objects.get(room_code=TEMP_CODE_ROOM).players_set.all()
        return context


class ResultRoomView(ListView):
    """Смотрим результаты"""

    template_name = 'game_1/room/result_room.html'
    context_object_name = 'players'

    def get_queryset(self):
        current_game = GameRoom.objects.get(room_code=TEMP_CODE_ROOM)
        select = current_game.players_set.all()
        return select
