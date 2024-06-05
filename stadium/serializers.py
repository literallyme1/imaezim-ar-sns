from rest_framework import serializers
from .models import User, GameResult

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'score']

class GameResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameResult
        fields = ['id', 'user', 'result', 'date_played']