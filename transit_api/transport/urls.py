from django.urls import path
from transport.views import RoadsView, VehiclesView

urlpatterns = [
    path('carreteras/', RoadsView.as_view(), name='carreteras'),
    path('vehicles/',   VehiclesView.as_view(),   name='vehicles'),
]