import datetime
import pathlib
import re
import time
import warnings

import pandas as pd
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from pandas.core.common import SettingWithCopyWarning
from sqlalchemy import create_engine

from geo.models import Demograficos

warnings.simplefilter(action="ignore", category=FutureWarning)
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)


class Command(BaseCommand):
    help = "Carga datos poblacionales"

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

        username = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        host = settings.DATABASES["default"]["HOST"]
        database = settings.DATABASES["default"]["NAME"]

        db_uri = f'postgresql://{username}:{password}@{host}:5432/{database}'

        self.engine = create_engine(db_uri).connect()

        self.columnas = ["object_id", "content_type_id", "fecha", "pobtot", "pobmas", "pobfem"]

    def add_arguments(self, parser):
        parser.add_argument("origen", type=str, help="Carpeta origen")

    def carga_datos(self, origen: str):
        fecha = int(re.findall(r"\d+", origen.split("/")[-1])[0])
        fecha = datetime.date(fecha, 1, 1)
        origen = pathlib.Path(origen)

        entidad_contenttype_id = ContentType.objects.get(model='entidad').id
        municipio_contenttype_id = ContentType.objects.get(model='municipio').id

        lista_df = [
            pd.read_csv(archivo, low_memory=False, encoding="utf-8")
            for archivo in origen.glob("*/conjunto_de_datos/*.csv")
            ]
        df = pd.concat(lista_df)
        df.columns = [columna.lower() for columna in df.columns]
        df.replace("*", 0, inplace=True)
        df['fecha'] = fecha

        # Entidad
        df_entidades = df[df["nom_loc"].str.contains("Total de la entidad")]
        df_entidades["object_id"] = df_entidades["entidad"].astype(str).str.zfill(2)
        df_entidades["content_type_id"] = entidad_contenttype_id
        df_entidades = df_entidades[self.columnas]
        df_entidades.reset_index(inplace=True, drop=True)
        df_entidades.to_sql(Demograficos._meta.db_table, con=self.engine, if_exists="append", index=False)

        # Municipio
        df_municipios = df[df["nom_loc"].str.contains("Total del municipio")]
        df_municipios["entidad"] = df_municipios["entidad"].astype(str).str.zfill(2)
        df_municipios["mun"] = df_municipios["mun"].astype(str).str.zfill(3)
        df_municipios["object_id"] = df_municipios["entidad"] + df_municipios["mun"]
        df_municipios["content_type_id"] = municipio_contenttype_id
        df_municipios = df_municipios[self.columnas]
        df_municipios.reset_index(inplace=True, drop=True)
        df_municipios.to_sql(Demograficos._meta.db_table, con=self.engine, if_exists="append", index=False)

    def handle(self, *args, **kwargs):
        origen = kwargs["origen"]
        self.stdout.write(self.style.NOTICE('Cargando censo'))
        start_time = time.time()
        self.carga_datos(origen)
        tiempo = time.time() - start_time
        self.stdout.write(self.style.NOTICE(f'Tiempo transcurrido: {tiempo / 60} minutos'))
