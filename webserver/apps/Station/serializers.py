

from rest_framework import serializers
from .models import  GridInfo,StationInfo

class GridInfoSerializer(serializers.ModelSerializer):
    # 注意此处不要继承错了，不要继承：serializers.Serializer
     class Meta:
         model=GridInfo
         fields = ('name', 'code', 'area')

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model=StationInfo
        fields=('__all__')

