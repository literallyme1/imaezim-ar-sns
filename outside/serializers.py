from rest_framework import serializers
from .models import OutPost, OutText, OutPicture, OutRecord, OutVideo, OutComment

class OutPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutPost
        fields = "__all__"

class OutTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutText
        fields = "__all__"

class OutPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutPicture
        fields = "__all__"

class OutRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutRecord
        fields = "__all__"

class OutVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutVideo
        fields = "__all__"

class OutCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutComment
        fields = "__all__"

class OutMemoInfoSerializer(serializers.ModelSerializer):  #메모의 타입에 따라 memo_content 추가하기
    memo_content = serializers.SerializerMethodField()

    class Meta:
        model = OutPost
        fields = ('id', 'userId', 'date', 'memoType', 'objectNumber', 'latitude', 'longitude', 'altitude', 'eunRotationX', 'eunRotationY','eunRotationZ','eunRotationW','open', 'memo_content')

    def get_memo_content(self, obj):
        if obj.memoType == 'A':    #text
            text_instance = OutText.objects.filter(id=obj.objectNumber).first()   #objectNumber와 Text의 id 같은 경우 찾아서 memo_content에 넣기
            if text_instance:
                serializer = OutTextSerializer(text_instance)
                return serializer.data
        elif obj.memoType == 'B':    #picture
            picture_instance = OutPicture.objects.filter(id=obj.objectNumber).first()
            if picture_instance:
                serializer = OutPictureSerializer(picture_instance)
                return serializer.data
        elif obj.memoType == 'C':    #record
            record_instance = OutRecord.objects.filter(id=obj.objectNumber).first()
            if record_instance:
                serializer = OutRecordSerializer(record_instance)
                return serializer.data
        elif obj.memoType == 'D':  # video
            video_instance = OutVideo.objects.filter(id=obj.objectNumber).first()
            if video_instance:
                serializer = OutVideoSerializer(video_instance)
                return serializer.data
        return None