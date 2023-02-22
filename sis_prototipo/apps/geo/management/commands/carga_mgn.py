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

from sis_prototipo.apps.geo.models import Entidad, Localidad, Manzana, Municipio

warnings.simplefilter(action="ignore", category=FutureWarning)


class Command(BaseCommand):
    help = "Prepara los datos para ingresar a la base de datos"

    def __init__(
        self, stdout=None, stderr=None, no_color=False, force_color=False
    ):
        super().__init__(stdout, stderr, no_color, force_color)
        self.map_ambito_localidad = dict(
            (y, x) for x, y in Localidad.AMBITO_TIPO
        )
        self.map_tipo = dict((y, x) for x, y in Manzana.MANZANA_TIPO)
        self.map_plano = dict((y, x) for x, y in Localidad.PLANO_TIPO)
        self.map_ambito_manzana = dict((y, x) for x, y in Manzana.AMBITO_TIPO)

        username = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        host = settings.DATABASES["default"]["HOST"]
        database = settings.DATABASES["default"]["NAME"]

        db_uri = f"postgresql://{username}:{password}@{host}:5432/{database}"

        self.columnas = [
            "pobtot",
            "pobmas",
            "pobfem",
        ]

        self.engine = create_engine(db_uri).connect()

    def add_arguments(self, parser):
        parser.add_argument(
            "mgn",
            nargs="?",
            type=str,
            help="Carpeta marco",
            default="data/mgn",
        )
        parser.add_argument(
            "censo",
            nargs="?",
            type=str,
            help="Carpeta censo",
            default="data/poblacion/censo2020",
        )

    def _procesa_censo(self, censo):
        lista_censo_df = [
            pd.read_csv(archivo, low_memory=False, encoding="utf-8")
            for archivo in pathlib.Path(censo).glob("*/conjunto_de_datos/*.csv")
        ]

        censo_df = pd.concat(lista_censo_df)

        censo_df.columns = [columna.lower() for columna in censo_df.columns]

        censo_df = censo_df[censo_df["nom_loc"] != "Total AGEB urbana"]

        censo_df.reset_index(drop=True, inplace=True)

        censo_df.replace("*", 0, inplace=True)

        censo_entidad_df = censo_df[censo_df['nom_loc'].str.contains('Total de la entidad')]
        censo_entidad_df = censo_entidad_df.drop(['nom_ent', 'mun', 'nom_mun', 'loc', 'nom_loc', 'ageb', 'mza'], axis=1)
        censo_entidad_df['entidad'] = censo_entidad_df['entidad'].astype(str).str.zfill(2)
        censo_entidad_df = censo_entidad_df.rename(columns={'entidad': 'cvegeo'})
        censo_entidad_df = censo_entidad_df[["cvegeo"] + self.columnas]

        censo_municipio_df = censo_df[censo_df['nom_loc'].str.contains('Total del municipio')]
        censo_municipio_df['entidad'] = censo_municipio_df['entidad'].astype(str).str.zfill(2)
        censo_municipio_df['mun'] = censo_municipio_df['mun'].astype(str).str.zfill(3)
        censo_municipio_df['cvegeo'] = censo_municipio_df['entidad'] + censo_municipio_df['mun']
        censo_municipio_df = censo_municipio_df[["cvegeo"] + self.columnas]

        censo_localidad_df = censo_df[censo_df['nom_loc'].str.contains('Total de la localidad urbana')]
        censo_localidad_df['entidad'] = censo_localidad_df['entidad'].astype(str).str.zfill(2)
        censo_localidad_df['mun'] = censo_localidad_df['mun'].astype(str).str.zfill(3)
        censo_localidad_df['loc'] = censo_localidad_df['loc'].astype(str).str.zfill(4)
        censo_localidad_df['cvegeo'] = censo_localidad_df['entidad'] + censo_localidad_df['mun'] + censo_localidad_df[
            'loc']
        censo_localidad_df = censo_localidad_df[["cvegeo"] + self.columnas]

        censo_manzana_df = censo_df[censo_df['mza'] != 0]
        censo_manzana_df['entidad'] = censo_manzana_df['entidad'].astype(str).str.zfill(2)
        censo_manzana_df['mun'] = censo_manzana_df['mun'].astype(str).str.zfill(3)
        censo_manzana_df['loc'] = censo_manzana_df['loc'].astype(str).str.zfill(4)
        censo_manzana_df['mza'] = censo_manzana_df['mza'].astype(str).str.zfill(3)
        censo_manzana_df['cvegeo'] = censo_manzana_df['entidad'] + censo_manzana_df['mun'] + censo_manzana_df['loc'] + \
                                     censo_manzana_df['ageb'] + censo_manzana_df['mza']
        censo_manzana_df = censo_manzana_df[["cvegeo"] + self.columnas]

        return censo_entidad_df, censo_municipio_df, censo_localidad_df, censo_manzana_df


    def _procesa_mgn(self, mgn):
        list_entidades = []
        list_municipios = []
        list_localidades = []
        list_manzanas = []

        estados = list(pathlib.Path(mgn).glob("*/conjunto_de_datos"))
        estados = sorted(
            estados, key=lambda x: int(str(x).split("/")[2].split("_")[0])
        )

        for archivo in estados:
            estado = archivo.parent.stem.split("_")[0]
            self.stdout.write(self.style.WARNING(f"Procesando {archivo}"))
            entidad_dir = archivo / f"{estado}ent.shp"
            municipio_dir = archivo / f"{estado}mun.shp"
            localidad_dir = archivo / f"{estado}l.shp"
            localidad_puntual_dir = archivo / f"{estado}lpr.shp"
            manzana_dir = archivo / f"{estado}m.shp"

            # Entidad
            df_entidad = gpd.read_file(
                entidad_dir, encoding="latin-1" #, crs="epsg:6372"
            )

            df_entidad["CVEGEO"] = df_entidad["CVEGEO"].astype(str).str.zfill(2)
            df_entidad["CVE_ENT"] = df_entidad["CVE_ENT"].astype(str).str.zfill(2)
            df_entidad["area"] = df_entidad["geometry"].area / 10**6
            df_entidad.columns = map(str.lower, df_entidad.columns)

            list_entidades.append(df_entidad)

            # Municipio
            df_municipio = gpd.read_file(
                municipio_dir, encoding="latin-1"# , crs="epsg:6372"
            )
            df_municipio["CVE_ENT"] = df_municipio["CVE_ENT"].astype(str).str.zfill(2)
            df_municipio["CVE_MUN"] = df_municipio["CVE_MUN"].astype(str).str.zfill(3)
            df_municipio["entidad_id"] = df_municipio["CVE_ENT"].astype(str)
            df_municipio["area"] = df_municipio["geometry"].area / 10**6
            df_municipio.columns = map(str.lower, df_municipio.columns)
            list_municipios.append(df_municipio)

            # Localidad
            df_localidad = gpd.read_file(
                localidad_dir, encoding="latin-1"# , crs="epsg:6372"
            )
            df_localidad["CVE_ENT"] = df_localidad["CVE_ENT"].astype(str).str.zfill(2)
            df_localidad["CVE_MUN"] = df_localidad["CVE_MUN"].astype(str).str.zfill(3)
            df_localidad["CVE_LOC"] = df_localidad["CVE_LOC"].astype(str).str.zfill(4)
            df_localidad["AMBITO"] = (
                df_localidad["AMBITO"]
                .map(self.map_ambito_localidad)
                .astype("int32")
            )
            df_localidad["municipio_id"] = df_localidad["CVE_ENT"].astype(
                str
            ) + df_localidad["CVE_MUN"].astype(str)
            df_localidad["area"] = df_localidad["geometry"].area / 10**6
            df_localidad.columns = map(str.lower, df_localidad.columns)
            list_localidades.append(df_localidad)

            # # Localidad puntual
            # df_localidad_puntual = gpd.read_file(
            #     localidad_puntual_dir, encoding="latin-1"# , crs="epsg:6372"
            # )
            # df_localidad_puntual["PLANO"] = (
            #     df_localidad_puntual["PLANO"]
            #     .map(self.map_plano)
            #     .astype("int32")
            # )
            # df_localidad_puntual["municipio_id"] = df_localidad_puntual[
            #     "CVE_ENT"
            # ].astype(str) + df_localidad_puntual["CVE_MUN"].astype(str)
            # df_localidad_puntual["CVEGEO"] = (
            #     df_localidad_puntual["CVE_ENT"].astype(str)
            #     + df_localidad_puntual["CVE_MUN"].astype(str)
            #     + df_localidad_puntual["CVE_LOC"].astype(str)
            # )
            # df_localidad_puntual.drop("CVE_MZA", axis=1, inplace=True)
            # df_localidad_puntual.drop("CVE_AGEB", axis=1, inplace=True)
            # list_localidades_puntuales.append(df_localidad_puntual)

            # Manzana
            df_manzana = gpd.read_file(
                manzana_dir, encoding="latin-1"# , crs="epsg:6372"
            )
            df_manzana["CVE_ENT"] = df_manzana["CVE_ENT"].astype(str).str.zfill(2)
            df_manzana["CVE_MUN"] = df_manzana["CVE_MUN"].astype(str).str.zfill(3)
            df_manzana["CVE_LOC"] = df_manzana["CVE_LOC"].astype(str).str.zfill(4)
            df_manzana["AMBITO"] = (
                df_manzana["AMBITO"]
                .map(self.map_ambito_manzana)
                .astype("int32")
            )
            df_manzana["TIPOMZA"] = (
                df_manzana["TIPOMZA"].map(self.map_tipo).astype("int32")
            )
            df_manzana["localidad_id"] = (
                df_manzana["CVE_ENT"].astype(str)
                + df_manzana["CVE_MUN"].astype(str)
                + df_manzana["CVE_LOC"].astype(str)
            )
            df_manzana["area"] = df_manzana["geometry"].area / 10**6
            df_manzana.columns = map(str.lower, df_manzana.columns)
            list_manzanas.append(df_manzana)
        return list_entidades, list_municipios, list_localidades, list_manzanas


    def _une_datos(self,
                  list_entidades,
                  list_municipios,
                  list_localidades,
                  list_manzanas,
                  censo_entidad_df,
                  censo_municipio_df,
                  censo_localidad_df,
                  censo_manzana_df):

        entidades = gpd.GeoDataFrame(pd.concat(list_entidades)# , crs="epsg:6372"
                                     )
        entidades["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature
            for feature in entidades["geometry"]
        ]
        entidades = entidades.rename(columns={"geometry": "geom"}).set_geometry(
            "geom"
        )
        entidades.to_crs(crs=settings.CRS, inplace=True)

        entidades = gpd.GeoDataFrame(
            pd.merge(entidades, censo_entidad_df, on='cvegeo')
        )
        entidades["densidad"] = entidades["pobtot"] / entidades["area"]

        municipios = gpd.GeoDataFrame(
            pd.concat(list_municipios)# , crs="epsg:6372"
        )
        municipios["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature
            for feature in municipios["geometry"]
        ]
        municipios = municipios.rename(
            columns={"geometry": "geom"}
        ).set_geometry("geom")
        municipios.to_crs(crs=settings.CRS, inplace=True)
        municipios = gpd.GeoDataFrame(
            pd.merge(municipios, censo_municipio_df, on='cvegeo')
        )
        municipios["densidad"] = municipios["pobtot"] / municipios["area"]
        localidades = gpd.GeoDataFrame(
            pd.concat(list_localidades)# , crs="epsg:6372"
        )
        localidades["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature
            for feature in localidades["geometry"]
        ]
        localidades["puntual"] = False
        localidades = localidades.rename(
            columns={"geometry": "geom"}
        ).set_geometry("geom")
        localidades.to_crs(crs=settings.CRS, inplace=True)

        localidades = gpd.GeoDataFrame(
            pd.merge(localidades, censo_localidad_df, on='cvegeo')
        )
        localidades["densidad"] = localidades["pobtot"] / localidades["area"]
        manzanas = gpd.GeoDataFrame(pd.concat(list_manzanas)# , crs="epsg:6372"
                                    )
        manzanas["geometry"] = [
            MultiPolygon([feature]) if isinstance(feature, Polygon) else feature
            for feature in manzanas["geometry"]
        ]
        manzanas = manzanas.rename(columns={"geometry": "geom"}).set_geometry(
            "geom"
        )
        manzanas.to_crs(crs=settings.CRS, inplace=True)
        manzanas = gpd.GeoDataFrame(
            pd.merge(manzanas, censo_manzana_df, on='cvegeo')
        )
        manzanas["densidad"] = manzanas["pobtot"] / manzanas["area"]
        return entidades, municipios, localidades, manzanas

    def _guarda_datos(self, entidades, municipios, localidades, manzanas):
        self.stdout.write(self.style.NOTICE("Insertando entidades"))
        entidades.to_postgis(
            Entidad._meta.db_table, self.engine, if_exists="append", index=False
        )

        self.stdout.write(self.style.NOTICE("Insertando municipios"))
        municipios.to_postgis(
            Municipio._meta.db_table,
            self.engine,
            if_exists="append",
            index=False,
        )

        self.stdout.write(self.style.NOTICE("Insertando localidades"))
        localidades.to_postgis(
            Localidad._meta.db_table,
            self.engine,
            if_exists="append",
            index=False,
        )


        self.stdout.write(self.style.NOTICE("Insertando manzanas"))
        manzanas.to_postgis(
            Manzana._meta.db_table, self.engine, if_exists="append", index=False
        )


    def carga_datos(self, mgn, censo):
        self.stdout.write(self.style.NOTICE("Procesando censo"))
        censo_entidad_df, censo_municipio_df, censo_localidad_df, censo_manzana_df = self._procesa_censo(censo)
        self.stdout.write(self.style.NOTICE("Procesando mgn"))
        list_entidades, list_municipios, list_localidades, list_manzanas = self._procesa_mgn(mgn)
        self.stdout.write(self.style.NOTICE("Uniendo datos"))
        entidades, municipios, localidades, manzanas = self._une_datos(
            list_entidades,
            list_municipios, 
            list_localidades,
            list_manzanas,
            censo_entidad_df,
            censo_municipio_df,
            censo_localidad_df,
            censo_manzana_df
        )
        self.stdout.write(self.style.NOTICE("Guardando datos"))
        self._guarda_datos(entidades, municipios, localidades, manzanas)


    def handle(self, *args, **kwargs):
        mgn = kwargs["mgn"]
        censo = kwargs["censo"]
        start_time = time.time()
        self.carga_datos(mgn, censo)
        tiempo = (time.time() - start_time) / 60
        self.stdout.write(
            self.style.SUCCESS(f"Tiempo transcurrido: {tiempo:3f} minutos")
        )