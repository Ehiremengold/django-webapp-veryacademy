from django.shortcuts import render

# Create your views here.
from hustle.models import Hustle
from .serializers import HustleSerilizer
from rest_framework.viewsets import ModelViewSet


class HustleViewSet(ModelViewSet):
    queryset = Hustle.objects.all().order_by()
    serializer_class = HustleSerilizer