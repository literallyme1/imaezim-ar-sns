from django.shortcuts import render
from .models import OutPost, OutText, OutPicture, OutRecord, OutVideo, OutComment
from common.models import User
from rest_framework import viewsets
from .serializers import OutPostSerializer, OutTextSerializer, OutPictureSerializer, OutRecordSerializer, OutVideoSerializer, OutCommentSerializer
from .serializers import OutMemoInfoSerializer
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import base64

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

        # 직렬화된 데이터를 Python 딕셔너리로 변환
        serialized_data = serializer_class.data

        # 각 객체에 대해 userId의 nickname을 추가
        for item in serialized_data:
            user_id = item['userId']
            user_instance = User.objects.get(pk=user_id)
            nickname = user_instance.nickname
            item['nickname'] = nickname


    return JsonResponse(serialized_data, safe=False)

def addMemo(request):  #새로운 메모 저장하기
    if request.method == 'POST':
        data = request.POST
        #타입에 따라 memo_content 저장
        if data.get('memoType') == 'A':  # Text
            out_text = OutText(text=data.get('memo_content'))  #받은 momo_content 저장
            out_text.save()
            saved_id = out_text.id  #저장된 id(PK)를 Post의 objectNumber에 저장
        elif data.get('memoType') == 'B':
            file = request.FILES['memo_content']
            if not file.name.lower().endswith(('.png', '.jpg', '.jpeg')): #파일이 이미지 확장자인지 확인
                return JsonResponse({'status': 'error', 'message': 'Not an image extension'})
            out_picture = OutPicture.objects.create(picture=file)
            out_picture.save()
            saved_id = out_picture.id
        elif data.get('memoType') == 'C':
            file = request.FILES['memo_content']
            if not file.name.lower().endswith(('.m4a', '.mp3')): #파일이 음성 확장자인지 확인
                return JsonResponse({'status': 'error', 'message': 'Not an audio extension'})
            out_record = OutRecord.objects.create(record=file)
            out_record.save()
            saved_id = out_record.id
        elif data.get('memoType') == 'D':
            file = request.FILES['memo_content']
            if not file.name.lower().endswith(('.mp4')): #파일이 영상 확장자인지 확인
                return JsonResponse({'status': 'error', 'message': 'Not an video extension'})
            out_video = OutVideo.objects.create(video=file)
            out_video.save()
            saved_id = out_video.id
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid memoType'})

        # 클라이언트에게 받은 userId에 해당하는 user 찾기
        try :
            # user_instance = User.objects.get(id=int(data.get('userId')))
            user_instance = User.objects.get(email=data.get('userId'))
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
                # eunRotation=data.get('eunRotation'),
                eunRotationX=data.get('eunRotationX'),
                eunRotationY=data.get('eunRotationY'),
                eunRotationZ=data.get('eunRotationZ'),
                eunRotationW=data.get('eunRotationW'),
                # open=data.get('open'),
            )
            out_post.save()
        except IntegrityError as e:
            error_message = str(e)
            print({'status': 'error', 'message': error_message})
            return JsonResponse({'status': 'error', 'message': error_message}) #post 저장 실패 시 오류 메시지

        return JsonResponse({'status': 'success'}) #저장 성공시 메시지

def get_last_Postid(request, email):
    user = User.objects.get(email=email) 
    UserModel = OutPost.objects.filter(userId=user).order_by('-id').first() #기본생성 id 가 가장 큰 거

    if UserModel:
        # 가장 마지막에 저장된 모델의 속성 값을 반환
        result = {'id': UserModel.id}
        return JsonResponse(result)
    else:
        # 해당 UserId에 해당하는 모델이 없을 경우 예외 처리
        return JsonResponse({'error': 'no UserId'})

def get_last_Image(request, email):
    user = User.objects.get(email=email) 
    UserModel = OutPost.objects.filter(userId=user).order_by('-id').first() #기본생성 id 가 가장 큰 거

    imageModel = OutPicture.objects.get(id = UserModel.objectNumber)
    if UserModel:
        # 가장 마지막에 저장된 모델의 속성 값을 반환
        result = {'picture': imageModel.picture.url}
        return JsonResponse(result)
    else:
        # 해당 UserId에 해당하는 모델이 없을 경우 예외 처리
        return JsonResponse({'error': 'no UserId'})


def get_last_Video(request, email):
    user = User.objects.get(email=email) 
    UserModel = OutPost.objects.filter(userId=user).order_by('-id').first() #기본생성 id 가 가장 큰 거

    imageModel = OutVideo.objects.get(id = UserModel.objectNumber)
    if UserModel:
        # 가장 마지막에 저장된 모델의 속성 값을 반환
        result = {'video': imageModel.video.url}
        return JsonResponse(result)
    else:
        # 해당 UserId에 해당하는 모델이 없을 경우 예외 처리
        return JsonResponse({'error': 'no UserId'})




