from rest_framework import serializers
from outside.models import OutPost, OutText, OutVideo, OutRecord, OutPicture
from inside.models import InPost, InText, InVideo, InRecord, InPicture
from inside.serializers import InPictureSerializer, InRecordSerializer, InVideoSerializer, InTextSerializer
from outside.serializers import OutPictureSerializer, OutRecordSerializer, OutVideoSerializer, OutTextSerializer
from django.core.serializers import serialize

class CombinedPostSerializer(serializers.Serializer): #outPost와 inPost 직렬화  #피드화면
    userId = serializers.IntegerField()
    date = serializers.DateField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    open = serializers.CharField(max_length=7)
    location_type = serializers.CharField()
    nickname = serializers.CharField(source='userId.nickname', read_only=True)
    detailAddr = serializers.CharField(max_length=50)

    def to_representation(self, instance):
        # instance는 OutPost or InPost #모델은 runtime에 결정됨
        location_type = 1 if isinstance(instance, OutPost) else 0  #실외 : 1  실내 : 0
        detailAddr = "" if isinstance(instance, OutPost) else instance.detailAddr  #실외의 경우 상세주소 : None
        return {
            'userId': instance.userId_id,
            'nickname': instance.userId.nickname,
            'location_type': location_type, #실외 실내 구분
            'date': instance.date,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'open': instance.open,
            'detailAddr' : detailAddr, #상세주소
        } #보내는 데이터 : 닉네임 날짜 위도 경도  실내or실외 상세주소   #1 -> 실외 0 -> 실내

class MyPageSerializer(serializers.Serializer):  #마이페이지
    #userId = serializers.IntegerField()
    #date = serializers.DateField()
    #latitude = serializers.FloatField()
    #longitude = serializers.FloatField()
    #open = serializers.CharField(max_length=7)
    #location_type = serializers.CharField()
    #nickname = serializers.CharField(source='userId.nickname', read_only=True)
    #detailAddr = serializers.CharField(max_length=50)
    #memoType = serializers.CharField(max_length=1)

    def to_representation(self, instance):
        # instance는 OutPost or InPost #모델은 runtime에 결정됨
        location_type = 1 if isinstance(instance, OutPost) else 0  #실외 : 1  실내 : 0
        detailAddr = "" if isinstance(instance, OutPost) else instance.detailAddr  #실외의 경우 상세주소 : None
        #메모 타입에 따른 메모 내용
        memoType = instance.memoType #메모 타입
        objectNum = instance.objectNumber #obj 넘버
        text = None
        picture = None
        record = None
        video = None
        if isinstance(instance, OutPost):  #실외
            if memoType == "A":
                outtext_instance = OutText.objects.filter(id=objectNum).first()  #objectNum에 해당하는 것반 필터링
                text = OutTextSerializer(outtext_instance).data['text'] if outtext_instance else None
            elif memoType == "B":
                outpicture_instance = OutPicture.objects.filter(id=objectNum).first()
                picture = OutPictureSerializer(outpicture_instance).data['picture'] if outpicture_instance else None
            elif memoType == "C":
                outrecord_instance = OutRecord.objects.filter(id=objectNum).first()
                record = OutRecordSerializer(outrecord_instance).data['record'] if outrecord_instance else None
            elif memoType == "D":
                outvideo_instance = OutVideo.objects.filter(id=objectNum).first()
                video = OutVideoSerializer(outvideo_instance).data['video'] if outvideo_instance else None

        elif isinstance(instance, InPost):  #실내
            if memoType == "A":
                intext_instance = InText.objects.filter(id=objectNum).first()  # objectNum에 해당하는 것반 필터링
                text = InTextSerializer(intext_instance).data['text'] if intext_instance else None
            elif memoType == "B":
                inpicture_instance = InPicture.objects.filter(id=objectNum).first()
                picture = InPictureSerializer(inpicture_instance).data['picture'] if inpicture_instance else None
            elif memoType == "C":
                inrecord_instance = InRecord.objects.filter(id=objectNum).first()
                record = InRecordSerializer(inrecord_instance).data['record'] if inrecord_instance else None
            elif memoType == "D":
                invideo_instance = InVideo.objects.filter(id=objectNum).first()
                video = InVideoSerializer(invideo_instance).data['video'] if invideo_instance else None

        return {
            'userId': instance.userId_id,
            'nickname': instance.userId.nickname,
            'location_type': location_type, #실외 실내 구분    #실외 : 1  실내 : 0
            'date': instance.date,
            'latitude': instance.latitude,
            'longitude': instance.longitude,
            'open': instance.open,
            'detailAddr': detailAddr, #상세주소
            'memoType': memoType,
            'text': text,
            'picture': picture,
            'record': record,
            'video': video,
        }

