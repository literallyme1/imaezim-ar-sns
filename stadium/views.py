from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, GameResult
from .serializers import UserSerializer, GameResultSerializer


class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GameResultListCreate(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        result = request.data.get('result')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if result == 'win':
            user.score += 100
        elif result == 'lose':
            user.score -= 50
        user.save()

        game_result = GameResult(user=user, result=result)
        game_result.save()

        return Response({'user': UserSerializer(user).data, 'game_result': GameResultSerializer(game_result).data})


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RankingList(APIView):
    def get(self, request, *args, **kwargs):
        top_users = User.objects.all().order_by('-score')[:10]
        serializer = UserSerializer(top_users, many=True)
        return Response(serializer.data)

