from django.contrib.auth.models import User
from django.db import models



class GameRoom(models.Model):
    room_code = models.CharField(max_length=4) # max_lenght=4
    create_time = models.DateTimeField(auto_now=True)
    is_end = models.BooleanField(default=False)

    def __str__(self):
        return str(self.room_code)


class Players(models.Model):
    parent_room = models.ForeignKey('GameRoom', on_delete=models.PROTECT, blank=True, null=True)
    player = models.ForeignKey(User, on_delete=models.PROTECT)
    round = models.IntegerField(blank=True, default=1)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.player)

