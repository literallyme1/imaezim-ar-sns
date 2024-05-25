from django.db import models
from common.models import User



#경복궁 퀴즈 관리
class Gyeongbokgung(models.Model):
    quizId = models.AutoField(primary_key=True)
    #GPS 기반
    latitude = models.FloatField()  #위도
    longitude = models.FloatField()  #경도
    altitude = models.FloatField()  #고도
    eunRotationX = models.FloatField(default=0.0)
    eunRotationY = models.FloatField(default=0.0)
    eunRotationZ = models.FloatField(default=0.0)
    eunRotationW = models.FloatField(default=0.0)  # 회전각도
    content = models.TextField() #나중에 그림 등도 추가 가능
    answer = models.TextField()

#사용자가 맞은 퀴즈 (개수를 이요해 stamp 부여)
class correctQuizInGyeongbokgung(models.Model):
    quizId = models.ForeignKey(Gyeongbokgung, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('quizId', 'userId') #같은 조합이 또 나오면 안된다.(무시함)


#Stamp 획득 여부
class Stamp(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)   
    GyeongbokgungStamp = models.BooleanField(default= False)
