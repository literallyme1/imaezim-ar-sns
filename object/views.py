from django.shortcuts import render
from django.http import JsonResponse
import cv2
from rembg import remove
from object import descriptor
import numpy as np
from django.db import IntegrityError
from .models import ObjectDesc, ObjText
from common.models import User
from rest_framework import viewsets
from .serializers import ObjectDescSerializer, ObjTextSerializer
from django.conf import settings
import os
import uuid


class Desc_drf(viewsets.ModelViewSet):
    queryset = ObjectDesc.objects.all()
    serializer_class = ObjectDescSerializer

class Text_drf(viewsets.ModelViewSet):
    queryset = ObjText.objects.all()
    serializer_class = ObjTextSerializer

# Create your views here.
def addObj(request):
    if request.method == 'POST':
        #data = request.POST
        file_list = []
        for i in range(1, 11):
            file_key = 'obj_img{}'.format(i) #obj1 ~ obj10으로 사진 10장
            if file_key in request.FILES:
                file_list.append(request.FILES[file_key])
        #특징점 추출
        detector_orb = cv2.ORB_create()
        all_features = []
        first_features = []
        for i, file in enumerate(file_list):
            nparr = np.fromstring(file.read(), np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            # 이미지 크기 조정
            height, width, _ = image.shape
            if height >= width:
                max_length = height
            else:
                max_length = width
            if max_length >= 1400:
                ratio = 1400 / max_length
                image = cv2.resize(image, (int(width * ratio), int(height * ratio)), interpolation=cv2.INTER_AREA)
            image_result = remove(image)  # 배경 제거
            _, desc = detector_orb.detectAndCompute(image_result, None)
            if i==0:
                first_features.append(desc)
            all_features.append(desc)

        #겹치는 특징점 제거
        filtered_features = descriptor.filter_matching_features_orb(all_features)
        if filtered_features.shape[0] < 2500:
            return JsonResponse({'status': 'Few feature points'}) #특징점 부족시 메시지
        #첫번째 사진으로 저장된 물건인지 확인
        old_obj_id = descriptor.findObj(first_features)

        #모델 저장
        desc_filename = str(uuid.uuid4()) + ".npy" #파일명 겹치지 않게
        desc_filepath = os.path.join(settings.MEDIA_ROOT, 'obj_desc', desc_filename)
        os.makedirs(os.path.dirname(desc_filepath), exist_ok=True)
        np.save(desc_filepath, filtered_features)
        try:
            obj_desc = ObjectDesc(
                desc=desc_filepath,
                img=file_list[0],
                #registration_completed
            )
            obj_desc.save()
        except IntegrityError as e:
            error_message = str(e)
            return JsonResponse({'status': 'error', 'message': error_message})  # post 저장 실패 시 오류 메시지
    old_obj_img=""
    if old_obj_id != -1:
        old_desc = ObjectDesc.objects.filter(id=old_obj_id).first()
        old_obj_img = old_desc.img.path
    return JsonResponse({'status': 'success', 'new_obj_id': obj_desc.id, 'old_obj_id': old_obj_id, 'old_obj_img': old_obj_img})  # 저장 성공시 메시지

def addText(request):
    data = request.POST
    #print(data.get('del_objId'))
    del_objId = int(data.get('del_objId'))
    objId = int(data.get('objId'))
    if del_objId != -1:
        del_desc = ObjectDesc.objects.filter(id=del_objId).first()
        if del_desc.registration_completed == False:
            del_desc_path = del_desc.desc.path
            del_img_path = del_desc.img.path
            if os.path.exists(del_desc_path):
                os.remove(del_desc_path)
            if os.path.exists(del_img_path):
                os.remove(del_img_path)
            del_desc.delete() #저장 미완료된 특징점 삭제
            print('특징점 삭제')
    obj_desc = ObjectDesc.objects.filter(id=objId).first()
    if obj_desc.registration_completed == False:
        obj_desc.registration_completed = True
        obj_desc.save() #저장 완료로 변경
        print('저장 완료로 변경')
    try:
        obj_text = ObjText(
            objId=ObjectDesc.objects.get(id=objId),
            userId=User.objects.get(pk=data.get('userId')),
            text=data.get('text'),
            open=data.get('open'),
        )
        obj_text.save()
    except IntegrityError as e:
        error_message = str(e)
        return JsonResponse({'status': 'error', 'message': error_message})  # post 저장 실패 시 오류 메시지
    return JsonResponse({'status': 'success'})  # 저장 성공시

def searchObj(request):
    return JsonResponse({'status': 'success'})  # 조회 성공시