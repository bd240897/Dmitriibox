from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from game_1.models import Players, AnswerPlayers


class RegisterUserForm(UserCreationForm):
    """Форма регитсрации"""

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class AnswerForm(forms.ModelForm):
    """Ответы игроков"""

    class Meta:
        parm_answer = {"type": "text",
                       "class": "form-control",
                       "placeholder": "Напишите Ваше сообщение",
                       "style": "height: 200px", }

        param_round = {"type": "text",
                       "class": "form-control",
                       "placeholder": "Напишите номер раунда",}

        model = AnswerPlayers
        fields = ('answer',)
        widgets = {
            'answer': forms.Textarea(attrs=parm_answer)
        }
#
# ########################3
# class AnswerSimpleForm(forms.Form):
#     """Простая форма для теста"""
#
#     answer = forms.Textarea()
#     round = forms.IntegerField()
#
# class TypingRoomView(View):
#     def get(self):
#         pass
#
#     def post(self):
#         pass
#
#         # # костыль костыль!!!!!
#         current_player = GameRoom.objects.get(room_code=TEMP_CODE_ROOM).players_set.last()
#         current_player.round = 1
#         current_player.answer = form.cleaned_data.get("answer")
#         current_player.parent_room = parent_room
#         current_player.save()
#         print()