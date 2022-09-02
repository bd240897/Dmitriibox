from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from game_1.models import AnswerPlayers, GameRoom


class RegisterUserForm(UserCreationForm):
    """Форма регитсрации"""

    parm_username = {"type": "text",
                     "class": "form-control",
                     "placeholder": "Ваше имя", }

    param_password1 = {"type": "text",
                       "class": "form-control",
                       "placeholder": "Ваш пароль", }

    param_password2 = {"type": "text",
                       "class": "form-control",
                       "placeholder": "Повторите пароль", }

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs=parm_username))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=param_password1))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs=param_password2))

    # class Meta:
    #     model = User
    #     fields = ('username', 'email', 'password1', 'password2')
    #     widgets = {
    #         'username': forms.TextInput(attrs={'class': 'form-input'}),
    #         'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
    #         'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
    #         'email': forms.EmailInput(attrs={'class': 'form-input'}),
    #     }


class LoginUserForm(AuthenticationForm):
    """Форма логина"""

    parm_username = {"type": "text",
                     "class": "form-control",
                     "placeholder": "Ваше имя", }

    param_password = {"type": "text",
                      "class": "form-control",
                      "placeholder": "Ваш пароль", }

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs=parm_username))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=param_password))

    # class Meta:
    #     parm_username = {"type": "text",
    #                      "class": "form-control",
    #                      "placeholder": "Напишите Ваше сообщение", }
    #
    #     param_password = {"type": "text",
    #                       "class": "form-control",
    #                       "placeholder": "Напишите номер раунда", }
    #
    #     fields = ('username', 'password')
    #
    #     widgets = {
    #         'username': forms.TextInput(attrs=parm_username),
    #         'password': forms.PasswordInput(attrs=param_password),
    #     }


class AnswerForm(forms.ModelForm):
    """Ответы игроков"""
    room_code = forms.HiddenInput()

    class Meta:
        parm_answer = {"type": "text",
                       "class": "form-control",
                       "placeholder": "Напишите Ваше сообщение",
                       "style": "height: 200px", }

        param_round = {"type": "text",
                       "class": "form-control",
                       "placeholder": "Напишите номер раунда", }

        model = AnswerPlayers
        fields = ('answer',)
        widgets = {
            'answer': forms.Textarea(attrs=parm_answer)
        }


class CreateRoomForm(forms.ModelForm):
    """Создать команату"""

    class Meta:
        param_room_code = {"type": "text",
                           "class": "form-control text-center",
                           "placeholder": "Номер комнаты",
                           "id": "room_code",
                           "value": "SQPQ"}

        model = GameRoom
        fields = ('room_code',)
        widgets = {
            'room_code': forms.TextInput(attrs=param_room_code)
        }
