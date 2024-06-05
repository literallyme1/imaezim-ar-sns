from django.urls import path, include
from .views import UserListCreate, GameResultListCreate, UserDetail, RankingList

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user_list_create'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('results/', GameResultListCreate.as_view(), name='game_result_list_create'),
    path('ranking/', RankingList.as_view(), name='ranking_list'),
]