from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView, ListView, DetailView, RedirectView
from ..forms import *

# //////////////////////////// LOGIN ////////////////////////////////////////


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