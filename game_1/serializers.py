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

################# ТЕСТИРУЮ Vue ######################
class GameRoomVueSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom
        fields = '__all__'

class AnswerPlayersSerializer(serializers.ModelSerializer):
    player = serializers.SerializerMethodField()

    def get_player(self, obj):
        return obj.player.username

    class Meta:
        model = AnswerPlayers
        fields = '__all__'

class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'

