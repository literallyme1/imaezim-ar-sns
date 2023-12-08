from django.urls import path, include
from rest_framework import routers
from SNS import views

router = routers.DefaultRouter()
#router.register('post_drf', views.PostView_drf)


urlpatterns = [
    #path('', include(router.urls)),
    path('feed/', views.CombinedPostView.as_view()),  #실내 & 실외 메모 -> feed 화면에 필요한 정보
    path('mypage/', views.MyPageView.as_view()),
]

