from django.contrib import admin
from .models import *

admin.site.register(GameRoom)
admin.site.register(AnswerPlayers)
admin.site.register(Questions)
admin.site.register(Rules)

# TODO create admin panel
# class PostAdmin(admin.ModelAdmin):
#     pass
#
# @admin.register(GameMain)
# class GameMainPostAdmin:
#     pass
#
# @admin.register(Players)
# class GameMainPlayersAdmin:
#     pass
