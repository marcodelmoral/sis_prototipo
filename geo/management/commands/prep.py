from django.core.management import BaseCommand

from geo.utils.prep_shp import preprocesa_shp


class Command(BaseCommand):
    help = "Prepara los datos para ingresar a la base de datos"

    def handle(self, *args, **options):
        preprocesa_shp()
