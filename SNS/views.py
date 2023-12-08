from django.shortcuts import render
from requests import Response

from outside.models import OutPost
from inside.models import InPost
from rest_framework.generics import ListAPIView
from .serializers import CombinedPostSerializer, MyPageSerializer
# Create your views here.

class CombinedPostView(ListAPIView):
    serializer_class = CombinedPostSerializer
    def get_queryset(self):
        # OutPost와 InPost에서 필요한 필드를 선택하여 합친 결과를 반환
        out_posts = OutPost.objects.all()
        in_posts = InPost.objects.all()

        combined_posts = list(out_posts) + list(in_posts)
        combined_posts.sort(key=lambda post: post.date, reverse=True) #최근 올린 메모순으로

        return combined_posts

class MyPageView(ListAPIView):  #마이페이지
    serializer_class = MyPageSerializer
    def get_queryset(self):
        getUserId = self.request.query_params.get('userId', None)  #클라이언트가 보낸 userId
        if getUserId is not None:
            # OutPost와 InPost에서 필요한 필드를 선택하여 합친 결과를 반환
            out_posts = OutPost.objects.filter(userId=getUserId)  #해당하는 userId만 보낸기
            in_posts = InPost.objects.filter(userId=getUserId)

            combined_posts = list(out_posts) + list(in_posts)
            combined_posts.sort(key=lambda post: post.date, reverse=True) #최근 올린 메모순으로

            return combined_posts
        else:
            return Response({'error': 'userid parameter is required'})
