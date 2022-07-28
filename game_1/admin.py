from django.contrib import admin

from .models import GameRoom, Players

admin.site.register(GameRoom)
admin.site.register(Players)

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
