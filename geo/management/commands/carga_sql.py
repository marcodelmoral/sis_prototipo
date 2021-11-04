from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Prepara los datos para ingresar a la base de datos"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("INEGI/sql/entidad.sql")
