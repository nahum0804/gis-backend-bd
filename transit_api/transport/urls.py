from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root_html),
    path('gps-data/', views.gps_data),
    path('vehiculos/', views.listar_vehiculos),
    path('vehiculos/<int:id>/posicion/',  views.posicion_actual),
    path('vehiculos/<int:id>/recorrido/', views.recorrido),
    path('vehiculos/<int:id>/prediccion/', views.prediccion),
    path('rutas/', views.listar_rutas),
    path('rutas/<int:id_ruta>/paradas', views.paradas_de_ruta),
]
