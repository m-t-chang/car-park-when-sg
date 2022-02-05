from rest_framework import serializers
from .models import Carpark, CarparkData


class CarparkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carpark
        fields = '__all__'


class CarparkDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarparkData
        fields = '__all__'
