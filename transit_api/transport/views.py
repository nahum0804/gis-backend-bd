from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

roads_data = {
    'type': 'FeatureCollection',
    'features': [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': [
                    [-84.0907, 9.9281],  # Cerca del Parque Central, SJ
                    [-84.0885, 9.9290],
                    [-84.0850, 9.9300],
                ]
            },
            'properties': {'f1': 1, 'f2': 'Ruta SJ Centro - Avenida Central'}
        },
        {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': [
                    [-84.0787, 9.9370],  # Barrio Amón
                    [-84.0765, 9.9380],
                    [-84.0740, 9.9390],
                ]
            },
            'properties': {'f1': 2, 'f2': 'Ruta Barrio Amón - Paseo Colón'}
        },
    ]
}

vehicles_data = [
  {'id':'bus-001','lat':10.362,'lng':-84.511,'routeId':1,'timestamp':'2025-06-19T12:00:00Z'},
  {'id':'bus-002','lat':10.360,'lng':-84.509,'routeId':1,'timestamp':'2025-06-19T12:00:05Z'},
]

class RoadsView(APIView):
    def get(self, request):
        return Response(roads_data, status=status.HTTP_200_OK)

class VehiclesView(APIView):
    def get(self, request):
        return Response(vehicles_data, status=status.HTTP_200_OK)