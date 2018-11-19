from rest_framework import serializers
from .models import  FubInfo,FubDataInfo

class FubInfoSerializer(serializers.ModelSerializer):
    # 注意此处不要继承错了，不要继承：serializers.Serializer
     class Meta:
         model=FubInfo
         fields = ('name', 'code', 'area')

class FubDataInfoSerializer(serializers.ModelSerializer):
    fid=FubInfoSerializer()
    class Meta:
        model=FubDataInfo
        fields=('__all__')