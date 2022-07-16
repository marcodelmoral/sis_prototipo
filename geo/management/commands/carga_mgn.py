import pathlib
import time
import warnings

import geopandas as gpd
import pandas as pd
from django.conf import settings
from django.core.management import BaseCommand
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
from sqlalchemy import create_engine

from geo.models import Entidad, Localidad, Manzana, Municipio

warnings.simplefilter(action="ignore", category=FutureWarning)


class Command(BaseCommand):
    help = "Prepara los datos para ingresar a la base de datos"

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.map_ambito_localidad = dict((y, x) for x, y in Localidad.AMBITO_TIPO)
        self.map_tipo = dict((y, x) for x, y in Manzana.MANZANA_TIPO)
        self.map_plano = dict((y, x) for x, y in Localidad.PLANO_TIPO)
        self.map_ambito_manzana = dict((y, x) for x, y in Manzana.AMBITO_TIPO)

        username = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        host = settings.DATABASES["default"]["HOST"]
        database = settings.DATABASES["default"]["NAME"]

        db_uri = f"postgresql://{username}:{password}@{host}:5432/{database}"

        self.engine = create_engine(db_uri).connect()

    def add_arguments(self, parser):
        parser.add_argument(
            "origen", nargs="?", type=str, help="Carpeta origen", default="data/mgn"
            )

    def procesa_shp(self, origen):
        list_entidades = []
        list_municipios = []
        list_localidades = []
        list_localidades_puntuales = []
        list_manzanas = []

        estados = list(pathlib.Path(origen).glob("*/conjunto_de_datos"))
        estados = sorted(estados, key=lambda x: int(str(x).split("/")[2].split("_")[0]))

        for archivo in estados:
            estado = archivo.parent.stem.split("_")[0]
            self.stdout.write(self.style.WARNING(f"Procesando {archivo}"))
            entidad_dir = archivo / f"{estado}ent.shp"
            municipio_dir = archivo / f"{estado}mun.shp"
            localidad_dir = archivo / f"{estado}l.shp"
            localidad_puntual_dir = archivo / f"{estado}lpr.shp"
            manzana_dir = archivo / f"{estado}m.shp"

            # Entidad
            df_entidad = gpd.read_file(entidad_dir, encoding="latin-1", crs="epsg:6372")
            list_entidades.append(df_entidad)

            # Municipio
            df_municipio = gpd.read_file(
                municipio_dir, encoding="latin-1", crs="epsg:6372"
                )
            df_municipio["entidad_id"] = df_municipio["CVE_ENT"].astype(str)
            list_municipios.append(df_municipio)

            # Localidad
            df_localidad = gpd.read_file(
                localidad_dir, encoding="latin-1", crs="epsg:6372"
                )
            df_localidad["AMBITO"] = (
                df_localidad["AMBITO"].map(self.map_ambito_localidad).astype("int32")
            )
            df_localidad["municipio_id"] = df_localidad["CVE_ENT"].astype(
                str
                ) + df_localidad["CVE_MUN"].astype(str)
            list_localidades.append(df_localidad)

            # Localidad puntual
            df_localidad_puntual = gpd.read_file(
                localidad_puntual_dir, encoding="latin-1", crs="epsg:6372"
                )
            df_localidad_puntual["PLANO"] = (
                df_localidad_puntual["PLANO"].map(self.map_plano).astype("int32")
            )
            df_localidad_puntual["municipio_id"] = df_localidad_puntual[
                                                       "CVE_ENT"
                                                   ].astype(str) + df_localidad_puntual["CVE_MUN"].astype(str)
            df_localidad_puntual["CVEGEO"] = (
                    df_localidad_puntual["CVE_ENT"].astype(str)
                    + df_localidad_puntual["CVE_MUN"].astype(str)
                    + df_localidad_puntual["CVE_LOC"].astype(str)
            )
            df_localidad_puntual.drop("CVE_MZA", axis=1, inplace=True)
            df_localidad_puntual.drop("CVE_AGEB", axis=1, inplace=True)
            list_localidades_puntuales.append(df_localidad_puntual)

            # Manzana
            df_manzana = gpd.read_file(manzana_dir, encoding="latin-1", crs="epsg:6372")
            df_manzana["AMBITO"] = (
                df_manzana["AMBITO"].map(self.map_ambito_manzana).astype("int32")
            )
            df_manzana["TIPOMZA"] = (
                df_manzana["TIPOMZA"].map(self.map_tipo).astype("int32")
            )
            df_manzana["localidad_id"] = (
                    df_manzana["CVE_ENT"].astype(str)
                    + df_manzana["CVE_MUN"].astype(str)
                    + df_manzana["CVE_LOC"].astype(str)
            )
            list_manzanas.append(df_manzana)

        entidades = gpd.GeoDataFrame(pd.concat(list_entidades), crs="epsg:6372")
        entidades["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature
            for feature in entidades["geometry"]
            ]
        entidades.to_crs(crs=settings.CRS, inplace=True)
        municipios = gpd.GeoDataFrame(pd.concat(list_municipios), crs="epsg:6372")
        municipios["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature
            for feature in municipios["geometry"]
            ]
        municipios.to_crs(crs=settings.CRS, inplace=True)
        localidades = gpd.GeoDataFrame(pd.concat(list_localidades), crs="epsg:6372")
        localidades["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature
            for feature in localidades["geometry"]
            ]
        localidades["puntual"] = False
        localidades.to_crs(crs=settings.CRS, inplace=True)
        localidades_puntual = gpd.GeoDataFrame(
            pd.concat(list_localidades_puntuales), crs="epsg:6372"
            )
        localidades_puntual["puntual"] = True
        localidades_puntual = localidades_puntual[
            ~localidades_puntual["CVEGEO"].isin(localidades["CVEGEO"])
        ]
        localidades_puntual.to_crs(crs=settings.CRS, inplace=True)
        manzanas = gpd.GeoDataFrame(pd.concat(list_manzanas), crs="epsg:6372")
        manzanas.to_crs(crs=settings.CRS, inplace=True)

        entidades.columns = map(str.lower, entidades.columns)
        municipios.columns = map(str.lower, municipios.columns)
        localidades.columns = map(str.lower, localidades.columns)
        localidades_puntual.columns = map(str.lower, localidades_puntual.columns)
        manzanas.columns = map(str.lower, manzanas.columns)

        self.stdout.write(self.style.NOTICE("Insertando entidades"))
        entidades.to_postgis(
            Entidad._meta.db_table, self.engine, if_exists="append", index=False
            )

        self.stdout.write(self.style.NOTICE("Insertando municipios"))
        municipios.to_postgis(
            Municipio._meta.db_table, self.engine, if_exists="append", index=False
            )

        self.stdout.write(self.style.NOTICE("Insertando localidades"))
        localidades.to_postgis(
            Localidad._meta.db_table, self.engine, if_exists="append", index=False
            )

        self.stdout.write(self.style.NOTICE("Insertando localidades puntuales"))
        localidades_puntual.to_postgis(
            Localidad._meta.db_table, self.engine, if_exists="append", index=False
            )

        self.stdout.write(self.style.NOTICE("Insertando manzanas"))
        manzanas.to_postgis(
            Manzana._meta.db_table, self.engine, if_exists="append", index=False
            )

    def handle(self, *args, **kwargs):
        origen = kwargs["origen"]
        self.stdout.write(self.style.WARNING("Procesando SHPs"))
        start_time = time.time()
        self.procesa_shp(origen)
        tiempo = (time.time() - start_time) / 60
        self.stdout.write(
            self.style.SUCCESS(f"Tiempo transcurrido: {tiempo:3f} minutos")
            )
