# //////////////////////////// URL FOR VUE ////////////////////////////////////////

class WaitingRoomAPI(RoomMixin, APIView):
    """ API """

    ACTION = {"next_room": "NEXT_ROOM",
              "start_game": "START_GAME"}

    name_current_view_room = 'waiting_room'

    # def get(self, request, *args, **kwargs):
    #     return Response({'massage': str(self.current_user) + " зашел в комнату " + str(self.room_code),
    #                      'next_url': reverse("typing_room", kwargs={'slug': self.room_code})
    #                      })

    def post(self, request, *args, **kwargs):

        # https://proproprogs.ru/django/drf-bazovyy-klass-apiview-dlya-predstavleniy
        action = request.data['action']  # {"action": "START_GAME"}
        if action == "START_GAME":
            # registration for vue
            # self.current_room.switch_game_status(self.request, self.current_user, "typing_room")
            return Response({'massage': "Got msg " + action,
                             'next_url': reverse("typing_room", kwargs={'slug': self.room_code})
                             })
        else:
            return Response({'error': "undefined action",
                             })


####### URL FOR VUE ########
# Start
# path('waiting/<slug:slug>/', WaitingRoomAPI.as_view(), name='waiting_room_API'),

# def is_room_exist(self):
#     room_code = self.request.data.get('room_code')
#     if not GameRoom.objects.filter(room_code=room_code).exists():
#         return Response({'massage': "Комнаты " + str(room_code) + " не существует!"})

# return Response({'success': "Massage sent",
#                  'massage': "vs_typing_room",
#                  'echo': JSONRenderer().render(dict(request.data))})