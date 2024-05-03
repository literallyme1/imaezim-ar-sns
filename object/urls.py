from django.urls import path, include
from object import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('desc_drf', views.Desc_drf)
router.register('text_drf', views.Text_drf)

urlpatterns = [
    path('', include(router.urls)),
    path('addObj/', views.addObj),
    path('addText/', views.addText),
    path('searchObj/', views.searchObj),
]

