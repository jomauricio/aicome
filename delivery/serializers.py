from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import Restaurante, Produto

class RestauranteSerializer(serializers.ModelSerializer):
    produtos = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='produtos-detail')
    class Meta:
        model = Restaurante
        fields = ['nome', 'endereco', 'fone', 'produtos']

class ProdutoSerializer(serializers.ModelSerializer):
    restaurante = serializers.StringRelatedField()
    class Meta:
        model = Produto
        fields = '__all__'