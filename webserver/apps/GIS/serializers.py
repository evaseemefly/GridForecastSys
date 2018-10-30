
from rest_framework import serializers

class WaveModelSerializer(serializers.Serializer):
    date=serializers.DateTimeField()
    value=serializers.FloatField()
