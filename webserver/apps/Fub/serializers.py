from rest_framework import serializers
from .models import  FubInfo,FubDataInfo,FubRealtimeInfo

class FubInfoSerializer(serializers.ModelSerializer):
    # 注意此处不要继承错了，不要继承：serializers.Serializer
     class Meta:
         model=FubInfo
         # fields = ('name', 'code', 'area','id')
         fields = ('__all__')


class FubDataInfoSerializer(serializers.ModelSerializer):
    fid=FubInfoSerializer()
    class Meta:
        model=FubDataInfo
        fields=('__all__')

class FubRealtimeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=FubRealtimeInfo
        fields=('__all__')

class FubRealtimeInfoMidSerializer(serializers.Serializer):
    '''
        海区及船舶集合
    '''
    ws=serializers.FloatField()
    wd=serializers.FloatField()
    # 气压
    bp = serializers.FloatField()
    # 有效波高
    wv = serializers.FloatField()
    # 有效周期
    wvperiod = serializers.FloatField()
    # 波向
    wvd = serializers.IntegerField()
    code = serializers.CharField()
    fid = serializers.IntegerField()
    # 时间戳
    # max_time=serializers.DateTimeField()
    timestamp=serializers.DateTimeField()
    # timestamp__max = serializers.DateTimeField()
    lon=serializers.FloatField()
    lat=serializers.FloatField()