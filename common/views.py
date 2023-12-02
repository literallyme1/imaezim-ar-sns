from django.shortcuts import render
from .models import User
from rest_framework import viewsets
from .serializers import UserSerializer


# Create your views here.
class UserView_drf(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer