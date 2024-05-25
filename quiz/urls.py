from django.urls import path, include
from rest_framework import routers
from inside import views
from .views import QuizAPIView, correctQuizInGyeongbokgungAPIView

urlpatterns = [
    path('quiz_api/', QuizAPIView.as_view()), #GET, POST
    path('quiz_api/<int:quizId>/', QuizAPIView.as_view()), #DELETE
    path('correct_quiz_api/', correctQuizInGyeongbokgungAPIView.as_view()), #POST
    path('correct_quiz_api/<int:userId>/', correctQuizInGyeongbokgungAPIView.as_view()), #GET
]