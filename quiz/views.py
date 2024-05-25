from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Gyeongbokgung, correctQuizInGyeongbokgung, Stamp
from .serializers import GyeongbokgungSerializer, correctQuizInGyeongbokgungSerializer
from rest_framework import status


#퀴즈를 gyeongbukgung 모델에 추가하고, 데이터를 불러온다.
class QuizAPIView(APIView):
    def get(self, request, **kwargs):
        quizzes = Gyeongbokgung.objects.all() #db 안에 있는 데이터 객체를 모두 가져옴
        serializer = GyeongbokgungSerializer(quizzes, many = True) #json 형식에 맞게 변환
        return Response(serializer.data)
    
    def post(self, request, **kwargs):
        serializer = GyeongbokgungSerializer(data = request.POST) 
        if serializer.is_valid(): #하나라도 null 이면 else 문 실행
            newInstance = serializer.save() 
            newPk = newInstance.quizId
            return Response({'message': 'Data saved successfully', 'pk': newPk}, status=201)
        else:
            return Response(serializer.errors, status=400) 
    
    def delete(self, request, **kwargs):
        quizId = kwargs.get('quizId')
        if quizId is not None:
            try:
                quiz = Gyeongbokgung.objects.get(quizId = quizId)
                quiz.delete()
                return Response({'message': 'GyeongbukgungData deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            except Gyeongbokgung.DoesNotExist:
                return Response({'error': 'GyeongbukgungData not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
                return Response({'error': 'deleteData not found'}, status=status.HTTP_404_NOT_FOUND)
        

class correctQuizInGyeongbokgungAPIView(APIView):
    def get(self, request, **kwargs):
        # user id 에 따른 quiz id (맞춘개수는 유니티에서)
        userId = kwargs.get('userId')
        if userId is not None:
            correctQuiz = correctQuizInGyeongbokgung.objects.filter(userId = userId)
            quizIds = list(correctQuiz.values_list('quizId', flat=True))
            return Response({'quizIds': quizIds})

    def post(self, request, **kwargs):
        serializer = correctQuizInGyeongbokgungSerializer(data = request.data)
        if serializer.is_valid(): #하나라도 null 이면 else 문 실행
            serializer.save() 
            return Response({'message': 'Data saved successfully'}, status=201)
        else:
            return Response(serializer.errors, status=400) 