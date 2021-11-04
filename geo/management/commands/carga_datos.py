# from geo.utils.load_infra import carga_infraestructura
import time

from django.core.management import BaseCommand

from geo.utils.load_pob2 import carga_poblacion


class Command(BaseCommand):
    help = "Carga archivos SHP, poblacionales y de infraestructura"

    def handle(self, *args, **options):
        start_time = time.time()
        # carga_shp()
        # carga_geojson()
        carga_poblacion()
        # carga_infraestructura()
        self.stdout.write(self.style.SUCCESS(f'Terminado en: {time.time() - start_time}'))
