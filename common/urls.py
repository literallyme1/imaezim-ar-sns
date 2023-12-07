from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from common import views

router = routers.DefaultRouter()
router.register('user_drf', views.UserView_drf)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', views.UserView),
]