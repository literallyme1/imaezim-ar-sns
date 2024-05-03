from django.db import models
from common.models import User

class ObjectDesc(models.Model):
    desc = models.FileField(upload_to='obj_desc/') #특징점
    img = models.ImageField(upload_to='obj_img/') #대표 이미지
    registration_completed = models.BooleanField(default=False)  #False : 등록중   True : 등록 완료

class ObjText(models.Model):
    objId = models.ForeignKey(ObjectDesc, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)  #날짜 자동으로 현재시각 저장
    text = models.TextField()
    open = models.CharField(max_length=7)   #전체공개:public  친구공개:friend  나만:private

"""
class ObjPicture(models.Model):
    objId = models.ForeignKey(ObjectDesc, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='picture/') #업로드 경로
    open = models.CharField(max_length=7)

class ObjRecord(models.Model):
    objId = models.ForeignKey(ObjectDesc, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    record = models.FileField(upload_to='record/')
    open = models.CharField(max_length=7)

class ObjVideo(models.Model):
    objId = models.ForeignKey(ObjectDesc, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    video = models.FileField(upload_to='video/')
    open = models.CharField(max_length=7)
"""