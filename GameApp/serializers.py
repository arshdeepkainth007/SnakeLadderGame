from rest_framework import serializers
from GameApp.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('GameID', 'P1Name', 'P2Name', 'Winner', 'CurrPlayer', 'P1Pos', 'P2Pos')