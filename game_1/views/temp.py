
############### В ЭТОМ ФАЙЛЕ СОБРАН ВОЗВРАТ В КОМНАТУ ПРИ ВЫХОДЕ СО СТРАНИЦЫ ###############

# возвращение в игру
# проверить статус комнаты
class WaitingRoomTestView(RoomMixin, CreateView):
    def temp(self):
        if self.current_room_status == self.name_current_view_room:
            pass
        else:
        # попытка вернутся в игру
            return HttpResponseRedirect(reverse("rejoin_game", kwargs={'slug': self.room_code}))


class TypingRoomView(RoomMixin, CreateView):
    @method_decorator(get_if_room_not_exist())
    def get(self, request, *args, **kwargs):

        # если игрок уже ответил на вопрос
        if not AnswerPlayers.objects.filter(player=self.current_user, round_of_answer=self.current_round).exists():
            pass
        else:
            return HttpResponseRedirect(reverse("waiting_typing_room", kwargs={'slug': self.room_code}))

        return super().get(self, request, *args, **kwargs)

class RejoinGameView(RoomMixin, View):
    """Возвращение в игру (чисто редирект)"""

    def get(self, *args, **kwargs):

        # возвращение в игру
        # TODO проверить статусы игры !!!!!!!!!!
        if self.is_user_in_room(): # self.current_room_status in ['typing', 'waiting', 'looking'] and
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