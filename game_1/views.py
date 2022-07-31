from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .logic import *
from .models import *
from .serializers import *


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


# ///////////////// КОМНАТЫ //////////////////////////

# class MainRoomView(TemplateView):
#     """
#     Главная страница игры
#     В каждую комнату нужно передавать ее КОД и НОМЕР РАЙНДА
#     МБ сделать это МИКСИНОМ через __init__
#     """
#
#     template_name = 'game_1/room/main_room.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['slug'] = 'SQPQ'
#         return super().get_context_data(**kwargs)


class RedirectMainRoomView(View):
    """Простой редирект на главную"""

    def get(self, *args, **kwargs):
        return redirect("main_room")


class MainRoomView(RoomMixin, CreateView):

    form_class = CreateRoomForm
    template_name = 'game_1/room/main_room.html'

    def get_context_data(self, **kwargs):

        # ЗАГЛУШКА ДЛЯ РАБОТЫ ПАНЕЛИ АДМИНА (МОЕЙ РУКОПИСНОЙ)
        kwargs['slug'] = 'SQPQ'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form_room_code = form.cleaned_data.get("room_code")
        self.create_room(room_code=form_room_code)
        print(form_room_code)
        return HttpResponseRedirect(reverse("waiting_room", kwargs={'slug': form_room_code}))

    # def get_success_url(self):
    #     return reverse_lazy('waiting_room')


# class WaitingRoomView(RoomMixin, TemplateView):
#     """Ожидание игроков"""
#
#     template_name = 'game_1/room/waiting_room_test.html'
#     template_name_main_room = 'game_1/room/main_room.html'
#
#     def get(self, *args, **kwargs):
#
#         """Если пользователь не авторизован отправить его на регистрацию"""
#         if not self.request.user.is_authenticated:
#             return redirect("game_login")
#
#         print('WaitingRoomView')
#
#         param_request_delete_players = self.request.GET.get("deleteplayers", 0)
#         param_request_delete_room = self.request.GET.get("deleteroom", 0)
#         param_request_join = self.request.GET.get("join", 0)
#         param_request_exit = self.request.GET.get("exit", 0)
#         param_request_create = self.request.GET.get("create", 0)
#         param_request_startgame = self.request.GET.get("startgame", 0)
#
#         # создать комнату
#         if param_request_create:
#             self.create_room()
#         # удалить комнату
#         elif param_request_delete_room:
#             self.delete_room()
#             return render(self.request, self.template_name_main_room)
#         # удалить игроков
#         elif param_request_delete_players:
#             self.delete_all_users(self.request)
#         # присоединиться к комнате
#         elif param_request_join:
#             self.join_to_game(self.request)
#         # выйти из комнаты
#         elif param_request_exit:
#             self.exit_to_game(self.request)
#         # начать игру
#         elif param_request_startgame:
#             self.start_game()
#             user = self.request.user
#             if not self.is_user_in_room(user):
#                 return super().get(*args, **kwargs)
#             return redirect("typing_room")
#
#         kwargs['players'] = self.players_in_game()
#         return super().get(*args, **kwargs)


class WaitingRoomTestView(RoomMixin, TemplateView):
    """Ожидание игроков"""
    """
    TO_DO выводить div с Игра уже идет. Игра еще не началась. и Кнопку начать игру убирать
    вынести round и room_codе в отдельный метод и запускать его в инит
    """

    template_name = 'game_1/room/waiting_room_test.html'
    template_name_main_room = 'game_1/room/main_room.html'

    def get(self, *args, **kwargs):

        """Если пользователь не авторизован отправить его на регистрацию"""
        if not self.request.user.is_authenticated:
            return redirect("game_login")

        # получим код текущей комнаты из запроса /<slug:slug>
        req_room_code = kwargs.get('slug')

        param_request_delete_players = self.request.GET.get("deleteplayers", 0)
        param_request_delete_room = self.request.GET.get("deleteroom", 0)
        param_request_join = self.request.GET.get("join", 0)
        param_request_exit = self.request.GET.get("exit", 0)
        param_request_create = self.request.GET.get("create", 0)
        param_request_startgame = self.request.GET.get("startgame", 0)

        # создать комнату
        if param_request_create:
            self.create_room(room_code=req_room_code)
        # удалить комнату
        elif param_request_delete_room:
            self.delete_room(room_code=req_room_code)
            return render(self.request, self.template_name_main_room)
        # удалить игроков
        elif param_request_delete_players:
            self.delete_all_users(room_code=req_room_code)
        # присоединиться к комнате
        elif param_request_join:
            self.join_to_game(room_code=req_room_code)
        # выйти из комнаты
        elif param_request_exit:
            self.exit_to_game(room_code=req_room_code)
        # начать игру
        elif param_request_startgame:
            self.start_game(room_code=req_room_code)
            user = self.request.user
            if not self.is_user_in_room(user):
                return super().get(*args, **kwargs)
            return redirect("typing_room")

        kwargs['players'] = self.players_in_game(room_code=req_room_code)
        return super().get(*args, **kwargs)


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

    # добавить проверку есть ли пользоватль в игре? и один ли он там!

    def setup(self, request, *args, **kwargs):
        self.room_code = kwargs.get('slug')
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.room_code = kwargs.get('slug')
        return super().post(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     """Получаем код текущей комнаты"""
    #
    #     return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Получаем вопрос из БД"""

        # считывает форму и создает запись с ответом пользователя
        current_room = self.get_current_room(room_code=TEMP_CODE_ROOM)
        current_round = current_room.round
        obj_question = get_object_or_404(Questions, round_for_question=current_round)
        kwargs['obj_question'] = obj_question
        kwargs['round'] = current_round

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # считывает форму и создает запись с ответом пользователя
        current_user = self.request.user
        current_room = self.get_current_room(room_code=self.room_code)
        current_player = current_room.players_set.get(player_in_room=current_user)  # !!!
        current_round = current_room.round

        AnswerPlayers.objects.create(player=current_player,
                                     answer=form.cleaned_data.get("answer"),
                                     round_of_answer=current_round)

        return HttpResponseRedirect(reverse("waiting_room", kwargs={'slug': self.room_code}))

    # def get_success_url(self):
    #     return reverse_lazy('waiting_typing_room')


class WaitingTypingRoomView(RoomMixin, TemplateView):
    """Ждем всех игроков после typing"""

    template_name = 'game_1/room/waiting_typing_room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_code = kwargs.get('slug')
        context['slug'] = room_code
        current_round = self.get_current_room(room_code=room_code).round
        context['players'] = AnswerPlayers.objects.filter(answer__isnull=False).filter(
            round_of_answer=current_round).filter(player__parent_room__room_code=room_code)
        context['round'] = current_round
        return context


class ResultRoomView(RoomMixin, ListView):
    """Смотрим результаты"""

    template_name = 'game_1/room/result_room.html'
    context_object_name = 'players'

    def get_queryset(self):
        current_round = self.get_current_room().round
        select = AnswerPlayers.objects.filter(answer__isnull=False).filter(round_of_answer=current_round).filter(
            player__parent_room__room_code=TEMP_CODE_ROOM)
        return select

    def get(self, *args, **kwargs):
        room_code = kwargs.get('slug')
        kwargs['slug'] = room_code

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
                return HttpResponseRedirect(reverse("typing_room", kwargs={'slug': room_code}))

        return super().get(self, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Получаем вопрос из БД"""
        # https://django.fun/ru/cbv/Django/3.0/django.views.generic.list/ListView/
        current_room = self.get_current_room()
        current_round = current_room.round

        # считывает форму и создает запись с ответом пользователя
        obj_question = get_object_or_404(Questions, round_for_question=current_round)
        kwargs['obj_question'] = obj_question
        kwargs['round'] = current_round

        room_code = kwargs.get('slug')
        kwargs['slug'] = room_code

        return super().get_context_data(*args, **kwargs)

    def is_questions_end(self):
        current_room = self.get_current_room()
        current_round = current_room.round
        return current_round >= MAX_ROUNDS


class GamveoverRoomView(RoomMixin, TemplateView):
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
        print("setup__113")
        print("**kwargs -", kwargs)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        print("dispatch")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("get")
        kwargs['find_method'] = ":::::::::"
        messages.success(request, '1 Profile updated successfully')
        messages.success(request, '2 Profile updated successfully')
        messages.success(request, '3 Profile updated successfully')

        return HttpResponseRedirect(reverse("find_2"))
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


class FindMethodsSecondView(TemplateView):
    """Проверка реверса"""

    template_name = 'game_1/find_methods.html'

    def get(self, request, *args, **kwargs):
        # kwargs['find_method_2'] = "3333333333"
        return super().get(request, *args, **kwargs)


class GetCurrentUsersAPI(ListAPIView):
    # queryset = Players.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset_users(self):
        req_room_code = self.kwargs['slug']
        select = Players.objects.filter(parent_room__room_code=req_room_code)  # .values_list("player_in_room")
        # получили объект класса Юзер
        select = [s.player_in_room for s in select]
        print("select", select)
        return select

    def get_queryset_gameroom(self):
        req_room_code = self.kwargs['slug']
        select = GameRoom.objects.get(room_code=req_room_code)
        return select

    def list(self, request, *args, **kwargs):
        queryset_users = self.get_queryset_users()
        serializer_users = UserSerializer(queryset_users, many=True)
        queryset_gameroom = self.get_queryset_gameroom()
        serializer_gameroom = GameRoomSerializer(queryset_gameroom, many=False)
        return Response({'users': serializer_users.data, 'gameroom': serializer_gameroom.data})

    # def list(self, request, *args, **kwargs):
    #     # https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/generic-views
    #     queryset = self.get_queryset()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response({'users': serializer.data})
