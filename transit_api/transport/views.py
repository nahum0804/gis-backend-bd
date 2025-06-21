from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import History, Vehiculos, Paradas
from .serializers import HistorySerializer
from datetime import datetime
from django.http import HttpResponse

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

@api_view(['GET'])
def listar_rutas(request):
    from .models import Rutas
    from .serializers import RutaSerializer

    rutas = Rutas.objects.all()
    serializer = RutaSerializer(rutas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def paradas_de_ruta(request, id_ruta):
    try:
        paradas = Paradas.objects.filter(id_ruta=id_ruta).order_by('orden')
        from .serializers import ParadaSerializer
        serializer = ParadaSerializer(paradas, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def api_root_html(request):
    html = """
    <html>
        <head><title>API Root</title></head>
        <body>
            <h1>Bienvenido a la API del sistema de transporte</h1>
            <ul>
                <li><a href="/api/gps-data/">GPS Data (POST)</a></li>
                <li><a href="/api/vehiculos/1/posicion">Posición actual de Vehículo ID 1</a></li>
                <li><a href="/api/vehiculos/1/recorrido">Recorrido del Vehículo ID 1</a></li>
                <li><a href="/api/vehiculos/1/prediccion">Predicción de llegada Vehículo ID 1</a></li>
                <li><a href="/api/rutas/">Lista de Rutas</a></li>
                <li><a href="/api/rutas/1/paradas">Paradas de la Ruta ID 1</a></li>
            </ul>
        </body>
    </html>
    """
    return HttpResponse(html)