from django.shortcuts import render
from .models import OutPost, OutText, OutPicture, OutRecord, OutVideo, OutComment
from common.models import User
from rest_framework import viewsets
from .serializers import OutPostSerializer, OutTextSerializer, OutPictureSerializer, OutRecordSerializer, OutVideoSerializer, OutCommentSerializer
from .serializers import OutMemoInfoSerializer
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

# Create your views here.
class PostView_drf(viewsets.ModelViewSet):
    queryset = OutPost.objects.all()
    serializer_class = OutPostSerializer

class TextView_drf(viewsets.ModelViewSet):
    queryset = OutText.objects.all()
    serializer_class = OutTextSerializer

class PictureView_drf(viewsets.ModelViewSet):
    queryset = OutPicture.objects.all()
    serializer_class = OutPictureSerializer

class RecordView_drf(viewsets.ModelViewSet):
    queryset = OutRecord.objects.all()
    serializer_class = OutRecordSerializer

class VideoView_drf(viewsets.ModelViewSet):
    queryset = OutVideo.objects.all()
    serializer_class = OutVideoSerializer

class CommentView_drf(viewsets.ModelViewSet):
    queryset = OutComment.objects.all()
    serializer_class = OutCommentSerializer

def MemoInfo(request):  #메모 정보 모두 받아오기
    if request.method == 'GET':
        queryset = OutPost.objects.all()
        serializer_class = OutMemoInfoSerializer(queryset, many=True)
        return JsonResponse(serializer_class.data, safe=False)

def addMemo(request):  #새로운 메모 저장하기
    if request.method == 'POST':
        data = request.POST
        #타입에 따라 memo_content 저장
        if data.get('memoType') == 'A':  # Text
            out_text = OutText(text=data.get('memo_content'))  #받은 momo_content 저장
            out_text.save()
            saved_id = out_text.id  #저장된 id(PK)를 Post의 objectNumber에 저장
        elif data.get('memoType') == 'B':
            out_picture = OutPicture(text=data.get('memo_content'))
            out_picture.save()
            saved_id = out_picture.id
        elif data.get('memoType') == 'C':
            out_record = OutRecord(text=data.get('memo_content'))
            out_record.save()
            saved_id = out_record.id
        elif data.get('memoType') == 'D':
            out_record = OutRecord(text=data.get('memo_content'))
            out_record.save()
            saved_id = out_record.id
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid memoType'})

        # 클라이언트에게 받은 userId에 해당하는 user 찾기
        try :
            user_instance = User.objects.get(id=int(data.get('userId')))
        except ObjectDoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No member information'})   #user 정보가 존재하지 않을 때 오류 메시지

        #post 데이터 저장
        try:
            out_post = OutPost(
                userId=user_instance,
                memoType=data.get('memoType'),
                objectNumber=saved_id,
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                altitude=data.get('altitude'),
                eunRotation=data.get('eunRotation'),
                open=data.get('open'),
            )
            out_post.save()
        except IntegrityError as e:
            error_message = str(e)
            return JsonResponse({'status': 'error', 'message': error_message}) #post 저장 실패 시 오류 메시지

        return JsonResponse({'status': 'success'}) #저장 성공시 메시지



