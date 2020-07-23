from hustle.models import Hustle
from rest_framework.serializers import ModelSerializer


class HustleSerilizer(ModelSerializer):
    class Meta:
        model = Hustle
        fields = ["user", 'hustle_name', 'content', 'category', "travel_availability"]
