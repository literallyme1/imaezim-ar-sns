from django.shortcuts import render
from common.models import User
from .models import InPost, InText, InPicture, InRecord, InVideo, InComment
from rest_framework import viewsets
from .serializers import InPostSerializer, InTextSerializer, InPictureSerializer, InRecordSerializer, InVideoSerializer, InCommentSerializer
from .serializers import InMemoInfoSerializer
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

# Create your views here.
class PostView_drf(viewsets.ModelViewSet):
    queryset = InPost.objects.all()
    serializer_class = InPostSerializer

class TextView_drf(viewsets.ModelViewSet):
    queryset = InText.objects.all()
    serializer_class = InTextSerializer

class PictureView_drf(viewsets.ModelViewSet):
    queryset = InPicture.objects.all()
    serializer_class = InPictureSerializer

class RecordView_drf(viewsets.ModelViewSet):
    queryset = InRecord.objects.all()
    serializer_class = InRecordSerializer

class VideoView_drf(viewsets.ModelViewSet):
    queryset = InVideo.objects.all()
    serializer_class = InVideoSerializer

class CommentView_drf(viewsets.ModelViewSet):
    queryset = InComment.objects.all()
    serializer_class = InCommentSerializer

def MemoInfo(request):  #메모 정보
    if request.method == 'GET':
        queryset = InPost.objects.all()
        serializer_class = InMemoInfoSerializer(queryset, many=True)
        # 직렬화된 데이터를 Python 딕셔너리로 변환
        serialized_data = serializer_class.data

        # 각 객체에 대해 userId의 nickname을 추가
        for item in serialized_data:
            user_id = item['userId']
            user_instance = User.objects.get(pk=user_id)
            nickname = user_instance.nickname
            item['nickname'] = nickname
    return JsonResponse(serializer_class.data, safe=False)

def addMemo(request):  #새로운 메모 저장하기
    if request.method == 'POST':
        data = request.POST
        #타입에 따라 memo_content 저장
        if data.get('memoType') == 'A':  # Text
            in_text = InText(text=data.get('memo_content'))  #받은 momo_content 저장
            in_text.save()
            saved_id = in_text.id  #저장된 id(PK)를 Post의 objectNumber에 저장
        elif data.get('memoType') == 'B':
            file = request.FILES['memo_content']
            if not file.name.lower().endswith(('.png', '.jpg', '.jpeg')): #파일이 이미지 확장자인지 확인
                return JsonResponse({'status': 'error', 'message': 'Not an image extension'})
            in_picture = InPicture.objects.create(picture=file)
            in_picture.save()
            saved_id = in_picture.id
        elif data.get('memoType') == 'C':
            file = request.FILES['memo_content']
            if not file.name.lower().endswith(('.m4a', '.mp3')): #파일이 음성 확장자인지 확인
                return JsonResponse({'status': 'error', 'message': 'Not an audio extension'})
            in_record = InRecord.objects.create(record=file)
            in_record.save()
            saved_id = in_record.id
        elif data.get('memoType') == 'D':
            file = request.FILES['memo_content']
            if not file.name.lower().endswith(('.mp4')): #파일이 영상 확장자인지 확인
                return JsonResponse({'status': 'error', 'message': 'Not an video extension'})
            in_record = InVideo.objects.create(video=file)
            in_record.save()
            saved_id = in_record.id
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid memoType'})

        # 클라이언트에게 받은 userId에 해당하는 user 찾기
        try :
            user_instance = User.objects.get(id=int(data.get('userId')))
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No member information'})   #user 정보가 존재하지 않을 때 오류 메시지
        #post 데이터 저장
        try:
            in_post = InPost(
                userId=user_instance,
                anchorId=data.get('anchorId'),
                memoType=data.get('memoType'),
                objectNumber=saved_id,
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                open=data.get('open'),
                detailAddr=data.get('detailAddr'),
            )
            in_post.save()
        except IntegrityError as e:
            error_message = str(e)
            return JsonResponse({'status': 'error', 'message': error_message}) #post 저장 실패 시 오류 메시지

        return JsonResponse({'status': 'success'}) #저장 성공시 메시지

def Comment(request):  #postId 받아서 postId에 해당하는 댓글만 보냄
    if request.method == 'POST':
        data = request.POST
        PostId = data.get('postId')
        if PostId is None:
            return JsonResponse({'error': 'no PostId'})
        comments = InComment.objects.filter(postId=PostId).order_by('-date')
        serializer_class = InCommentSerializer(comments, many=True)
        return JsonResponse(serializer_class.data, safe=False)