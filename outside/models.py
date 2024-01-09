from django.db import models
from common.models import User

# Create your models here.
class OutPost(models.Model):
    # id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)  #날짜 자동으로 현재시각 저장
    memoType = models.CharField(max_length=1) #A:text  B:picture  C:record   D:video
    objectNumber = models.IntegerField()  #Text, Picture, Record, Video의 id와 동일한 값으로 넣어주기
    latitude = models.FloatField()  #위도
    longitude = models.FloatField()  #경도
    altitude = models.FloatField()  #고도
    eunRotationX = models.FloatField(default=0.0)
    eunRotationY = models.FloatField(default=0.0)
    eunRotationZ = models.FloatField(default=0.0)
    eunRotationW = models.FloatField(default=0.0)  # 회전각도
    open = models.CharField(max_length=7)   #전체공개:public  친구공개:friend  나만:private

class OutText(models.Model):
    text = models.TextField()

class OutPicture(models.Model):
    picture = models.ImageField(upload_to='picture/') #업로드 경로

class OutRecord(models.Model):
    record = models.FileField(upload_to='record/')

class OutVideo(models.Model):
    video = models.FileField(upload_to='video/')

class OutComment(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True) #날짜 자동으로 현재시각 저장
    postId = models.ForeignKey(OutPost, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
