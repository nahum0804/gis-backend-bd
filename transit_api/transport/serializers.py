from rest_framework import serializers
from .models import History, Vehiculos, Paradas, Rutas

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculos
        fields = '__all__'

class ParadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paradas
        fields = '__all__'

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rutas
        fields = '__all__'
