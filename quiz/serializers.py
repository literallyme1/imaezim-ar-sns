from rest_framework import serializers
from .models import Gyeongbokgung, correctQuizInGyeongbokgung


class GyeongbokgungSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gyeongbokgung
        fields = "__all__"

class correctQuizInGyeongbokgungSerializer(serializers.ModelSerializer):
    class Meta:
        model = correctQuizInGyeongbokgung
        fields = "__all__"
