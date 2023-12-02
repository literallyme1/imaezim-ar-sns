from django.urls import path, include
from rest_framework import routers
from outside import views

router = routers.DefaultRouter()
router.register('post_drf', views.PostView_drf)
router.register('text_drf', views.TextView_drf)
router.register('picture_drf', views.PictureView_drf)
router.register('record_drf', views.RecordView_drf)
router.register('video_drf', views.VideoView_drf)
router.register('comment_drf', views.CommentView_drf)

urlpatterns = [
    path('', include(router.urls)),
    path('memoInfo/', views.MemoInfo),  #메모 정보 url -> post 데이터와 각 메모타입에 따라 내용 추가해서 보여줌   #메모 정보 모두 받아오기
    path('addMemo/', views.addMemo),  #메모 저장 url
]

