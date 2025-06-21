from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import History, Vehiculos, Paradas
from .serializers import HistorySerializer
from datetime import datetime

@api_view(['POST'])
def gps_data(request):
    try:
        vehiculo_id = request.data['id_vehiculo']
        lat = float(request.data['lat'])
        lon = float(request.data['lon'])
        timestamp = request.data.get('timestamp', datetime.now())

        punto = Point(lon, lat)
        History.objects.create(id_vehiculo_id=vehiculo_id, geom=punto, timestamp=timestamp)

        return Response({'status': 'ok'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def posicion_actual(request, id):
    last = History.objects.filter(id_vehiculo=id).order_by('-timestamp').first()
    if not last:
        return Response({'error': 'Vehículo no encontrado'}, status=404)
    return Response({
        'vehiculo_id': id,
        'lat': last.geom.y,
        'lon': last.geom.x,
        'timestamp': last.timestamp
    })

@api_view(['GET'])
def recorrido(request, id):
    historial = History.objects.filter(id_vehiculo=id).order_by('timestamp')
    return Response(HistorySerializer(historial, many=True).data)

@api_view(['GET'])
def prediccion(request, id):
    ultimo = History.objects.filter(id_vehiculo=id).order_by('-timestamp').first()
    if not ultimo:
        return Response({'error': 'Sin posición'}, status=404)

    parada = Paradas.objects.annotate(
        distancia=Distance('geom', ultimo.geom)
    ).order_by('distancia').first()

    distancia_m = ultimo.geom.distance(parada.geom) * 111000  # aprox
    velocidad = 30  # km/h
    eta = distancia_m / (velocidad * 1000 / 60)

    return Response({
        'vehiculo_id': id,
        'parada_objetivo': parada.nombre,
        'distancia_metros': round(distancia_m, 2),
        'eta_minutos': round(eta, 2)
    })
