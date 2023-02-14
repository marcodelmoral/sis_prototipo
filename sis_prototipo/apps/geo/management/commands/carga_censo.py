import datetime
import pathlib
import re
import time
import warnings

import pandas as pd
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from sqlalchemy import create_engine

from sis_prototipo.apps.geo.models import Entidad, Municipio, Localidad, Manzana

warnings.filterwarnings('ignore')


class Command(BaseCommand):
    help = "Carga datos poblacionales"

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

        username = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        host = settings.DATABASES["default"]["HOST"]
        database = settings.DATABASES["default"]["NAME"]

        db_uri = f"postgresql://{username}:{password}@{host}:5432/{database}"

        self.engine = create_engine(db_uri).connect()

        self.columnas = [
            "pobtot",
            "pobmas",
            "pobfem",
        ]

    def add_arguments(self, parser):
        parser.add_argument("origen", nargs="?", type=str, help="Carpeta origen", default="data/poblacion/censo2020")

    def carga_datos(self, origen: str):

        origen = pathlib.Path(origen)

        lista_df = [
            pd.read_csv(archivo, low_memory=False, encoding="utf-8")
            for archivo in origen.glob("*/conjunto_de_datos/*.csv")
        ]

        df = pd.concat(lista_df)

        df.columns = [columna.lower() for columna in df.columns]

        df = df[df["nom_loc"] != "Total AGEB urbana"]

        df.reset_index(drop=True, inplace=True)

        df["entidad"] = df["entidad"].astype(str).str.zfill(2)
        df["mun"] = df["mun"].astype(str).str.zfill(3)
        df['loc'] = df['loc'].astype(str).str.zfill(4)
        df['mza'] = df['mza'].astype(str).str.zfill(3)

        df.replace("*", 0, inplace=True)

        # Todos
        df["cvegeo"] = None

        df['cvegeo'].loc[df['nom_loc'] == 'Total de la entidad'] = df["entidad"]

        df['cvegeo'].loc[df['nom_loc'] == 'Total del municipio'] = df["entidad"] + df["mun"]

        df['cvegeo'].loc[df['nom_loc'] == 'Total de la localidad urbana'] = df["entidad"] + df["mun"] + df["loc"]

        df['cvegeo'].loc[df['mza'] != "000"] = df["entidad"] + df["mun"] + df["loc"] + df["ageb"] + df["mza"]

        df = df[self.columnas]

        df_entidad = df[df["nom_loc"] == "Total de la entidad"].copy()
        df_mun = df[df["nom_loc"] == "Total del municipio"].copy()
        df_loc = df[df["nom_loc"] == "Total de la localidad urbana"].copy()
        df_mza = df[df["mza"] != "000"].copy()

        Entidad.objects.bulk_update(Entidad.objects.all(), self.columnas)
        Municipio.objects.bulk_update(Municipio.objects.all(), self.columnas)
        Localidad.objects.bulk_update(Localidad.objects.all(), self.columnas)
        Manzana.objects.bulk_update(Manzana.objects.all(), self.columnas)

    def handle(self, *args, **kwargs):
        origen = kwargs["origen"]
        self.stdout.write(self.style.WARNING("Cargando censo"))
        start_time = time.time()
        self.carga_datos(origen)
        tiempo = (time.time() - start_time) / 60
        self.stdout.write(
            self.style.SUCCESS(f"Tiempo transcurrido: {tiempo:.3f} minutos")
        )
