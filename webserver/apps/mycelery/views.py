from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import APIView

from .tasks import readFubXml
# Create your views here.
class Test(APIView):
    def get(self):
        readFubXml('201312051000qf101.dat.xml.xml')
        return Response()
