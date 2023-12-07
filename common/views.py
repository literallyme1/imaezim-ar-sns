from django.http import JsonResponse
from django.shortcuts import render
from .models import User
from rest_framework import viewsets
from .serializers import UserSerializer


# Create your views here.
class UserView_drf(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def UserView(request):  #email해당하는 User 정보 보내기
    if request.method == 'POST':
        get_email = request.POST.get('email', '')
        queryset = User.objects.filter(email=get_email)
        serializer_class = UserSerializer(queryset, many=True)
        return JsonResponse(serializer_class.data, safe=False)