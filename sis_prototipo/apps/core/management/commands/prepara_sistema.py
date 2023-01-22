import time

from django.core import management
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Prepara los datos para ingresar a la base de datos"

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

    def add_arguments(self, parser):
        parser.add_argument(
            "carpeta_mgn", nargs="?", type=str, help="Carpeta origen", default="data/mgn"
        )
        parser.add_argument(
            "carpeta_censo",
            nargs="?",
            type=str,
            help="Carpeta origen",
            default="data/poblacion/censo2020",
        )
        parser.add_argument(
            "archivo_dengue",
            nargs="?",
            type=str,
            help="Carpeta origen",
            default="data/dengue/data_vector.csv",
        )
        parser.add_argument(
            "archivo_agregados",
            nargs="?",
            type=str,
            help="Carpeta origen",
            default="data/agregagos/serie_final.csv",
        )

    def handle(self, *args, **kwargs):
        mgn = kwargs["carpeta_mgn"]
        censo = kwargs["carpeta_censo"]
        dengue = kwargs["archivo_dengue"]
        agregados = kwargs["archivo_agregados"]
        self.stdout.write(self.style.WARNING("Preparando el sistema"))
        start_time = time.time()
        management.call_command("carga_mgn")
        management.call_command("carga_censo")
        management.call_command("carga_agregados")
        management.call_command("carga_dengue")
        tiempo = (time.time() - start_time) / 60
        self.stdout.write(
            self.style.SUCCESS(f"Tiempo transcurrido: {tiempo:3f} minutos")
        )
