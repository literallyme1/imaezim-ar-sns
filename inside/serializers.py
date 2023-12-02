from rest_framework import serializers
from .models import InPost, InText, InPicture, InRecord, InVideo, InComment

class InPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = InPost
        fields = "__all__"

class InTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = InText
        fields = "__all__"

class InPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = InPicture
        fields = "__all__"

class InRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = InRecord
        fields = "__all__"

class InVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InVideo
        fields = "__all__"

class InCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InComment
        fields = "__all__"

class InMemoInfoSerializer(serializers.ModelSerializer):  #메모의 타입에 따라 memo_content 추가하기
    memo_content = serializers.SerializerMethodField()

    class Meta:
        model = InPost
        fields = ('id', 'anchorId', 'userId', 'date', 'memoType', 'objectNumber', 'latitude', 'longitude', 'open', 'memo_content')

    def get_memo_content(self, obj):
        if obj.memoType == 'A':    #text
            text_instance = InText.objects.filter(id=obj.objectNumber).first()   #objectNumber와 Text의 id 같은 경우 찾아서 memo_content에 넣기
            if text_instance:
                serializer = InTextSerializer(text_instance)
                return serializer.data
        elif obj.memoType == 'B':    #picture
            picture_instance = InPicture.objects.filter(id=obj.objectNumber).first()
            if picture_instance:
                serializer = InPictureSerializer(picture_instance)
                return serializer.data
        elif obj.memoType == 'C':    #record
            record_instance = InRecord.objects.filter(id=obj.objectNumber).first()
            if record_instance:
                serializer = InRecordSerializer(record_instance)
                return serializer.data
        elif obj.memoType == 'D':  # video
            video_instance = InVideo.objects.filter(id=obj.objectNumber).first()
            if video_instance:
                serializer = InVideoSerializer(video_instance)
                return serializer.data
        return None