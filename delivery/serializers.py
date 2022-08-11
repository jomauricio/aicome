from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Restaurante

class RestauranteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurante
        fields = '__all__'