from django.contrib.gis.db import models

class Rutas(models.Model):
    id_ruta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    geom = models.LineStringField(srid=4326)

    class Meta:
        db_table = 'rutas'
        managed = False  # Evita que Django intente crear o modificar esta tabla

class Paradas(models.Model):
    id_parada = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    orden = models.IntegerField()
    id_ruta = models.ForeignKey(Rutas, on_delete=models.CASCADE, db_column='id_ruta')
    geom = models.PointField(srid=4326)

    class Meta:
        db_table = 'paradas'
        managed = False

class Vehiculos(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    id_ruta = models.ForeignKey(Rutas, null=True, on_delete=models.SET_NULL, db_column='id_ruta')
    geom = models.PointField(srid=4326)

    class Meta:
        db_table = 'vehiculos'
        managed = False

class History(models.Model):
    id = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE, db_column='id_vehiculo')
    timestamp = models.DateTimeField()
    geom = models.PointField(srid=4326)

    class Meta:
        db_table = 'history'
        managed = False