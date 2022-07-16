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

from geo.models import Demograficos

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
            "object_id",
            "content_type_id",
            "fecha",
            "pobtot",
            "pobmas",
            "pobfem",
            ]

    def add_arguments(self, parser):
        parser.add_argument("origen", nargs="?", type=str, help="Carpeta origen", default="data/poblacion/censo2020")

    def carga_datos(self, origen: str):
        fecha = int(re.findall(r"\d+", origen.split("/")[-1])[0])
        fecha = datetime.date(fecha, 1, 1)
        origen = pathlib.Path(origen)

        entidad_contenttype_id = ContentType.objects.get(model="entidad").id
        municipio_contenttype_id = ContentType.objects.get(model="municipio").id
        localidad_contenttype_id = ContentType.objects.get(model="localidad").id
        manzana_contenttype_id = ContentType.objects.get(model="manzana").id

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

        df["fecha"] = fecha

        df["object_id"] = None
        df["content_type_id"] = None

        # Todos
        df['object_id'].loc[df['nom_loc'] == 'Total de la entidad'] = df["entidad"]
        df['content_type_id'].loc[df['nom_loc'] == 'Total de la entidad'] = entidad_contenttype_id

        df['object_id'].loc[df['nom_loc'] == 'Total del municipio'] = df["entidad"] + df["mun"]
        df['content_type_id'].loc[df['nom_loc'] == 'Total del municipio'] = municipio_contenttype_id

        df['object_id'].loc[df['nom_loc'] == 'Total de la localidad urbana'] = df["entidad"] + df["mun"] + df["loc"]
        df['content_type_id'].loc[df['nom_loc'] == 'Total de la localidad urbana'] = localidad_contenttype_id

        df['object_id'].loc[df['mza'] != "000"] = df["entidad"] + df["mun"] + df["loc"] + df["ageb"] + df["mza"]
        df['content_type_id'].loc[df['mza'] != "000"] = manzana_contenttype_id

        df = df[self.columnas]

        df.sort_values("object_id", inplace=True)

        df.to_sql(
            Demograficos._meta.db_table,
            con=self.engine,
            index=False,
            if_exists="append",
            method="multi",
            )

    def handle(self, *args, **kwargs):
        origen = kwargs["origen"]
        self.stdout.write(self.style.WARNING("Cargando censo"))
        start_time = time.time()
        self.carga_datos(origen)
        tiempo = (time.time() - start_time) / 60
        self.stdout.write(
            self.style.SUCCESS(f"Tiempo transcurrido: {tiempo:.3f} minutos")
            )
