from django.contrib import admin

from .models import *

admin.site.register(GameRoom)
admin.site.register(Players)
admin.site.register(AnswerPlayers)
admin.site.register(Questions)

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
