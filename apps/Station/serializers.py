

from rest_framework import serializers
from .models import  GridInfo

class GridInfoSerializer(serializers.ModelSerializer):
    # 注意此处不要继承错了，不要继承：serializers.Serializer
     class Meta:
         model=GridInfo
         fields = ('name', 'code', 'area')
