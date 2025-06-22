import psycopg2, pprint
from django.conf import settings 
params = {
    "dbname":   "proyectoIII",
    "user":     "postgres",
    "password": "1234",
    "host":     "192.168.1.79",
    "port":     5432,
}

conn = psycopg2.connect(**settings.DATABASES['default'])
print("¡Conexión OK!")