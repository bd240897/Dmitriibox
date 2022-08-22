from rest_framework import serializers

from .models import *




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username") #"__all__"

class GameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom
        fields = ("room_code", "status")

class GameStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom
        fields = ("room_code", "status")
        lookup_field = 'room_code'