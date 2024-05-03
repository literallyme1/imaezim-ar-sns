from rest_framework import serializers
from .models import ObjectDesc, ObjText

class ObjectDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectDesc
        fields = "__all__"

class ObjTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjText
        fields = "__all__"