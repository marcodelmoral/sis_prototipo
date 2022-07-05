import warnings

import geopandas as gpd
import pandas as pd
from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from sqlalchemy import create_engine

from dengue.models import Vector
from geo.models import Municipio

warnings.simplefilter(action='ignore', category=FutureWarning)


class Command(BaseCommand):
    help = ''

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.map_diagnostico = dict((y, x) for x, y in Vector.DIAGNOSTICO)
        self.columnas = [
            "fol_id",
            "ide_nom",
            "ide_ape_pat",
            "ide_ape_mat",
            "ide_sex",
            "num_ext",
            "ide_fec_nac",
            "ide_cal",
            "ide_cp",
            "ide_col",
            "des_ocupacion",
            "cve_diag_final",
            "fec_sol_aten",
            "municipio_id"
            ]
        username = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        host = settings.DATABASES["default"]["HOST"]
        database = settings.DATABASES["default"]["NAME"]

        db_uri = f'postgresql://{username}:{password}@{host}:5432/{database}'

        self.engine = create_engine(db_uri).connect()

    def add_arguments(self, parser):
        parser.add_argument('archivo', type=str, help='')

    def carga_datos(self, archivo):
        df = pd.read_csv(archivo, encoding="utf-8", index_col=None, low_memory=False)
        df = df.drop(columns=["Unnamed: 0"], axis=1)
        df.columns = [column.lower() for column in df.columns]
        df["ide_cal"] = df["des_cal"] + " " + df["ide_cal"]
        df_obj = df.select_dtypes(['object'])
        df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
        # df['cve_edo_res'] = df['cve_edo_res'].astype(str).str.zfill(2)
        # df['cve_mpo_res'] = df['cve_mpo_res'].astype(str).str.zfill(3)
        # df['cve_loc_res'] = df['cve_loc_res'].astype(str).str.zfill(4)

        # df['localidad_id'] = df['cve_edo_res'] + df['cve_mpo_res'] + df['cve_loc_res']
        # df['creado'] = df['fec_sol_aten']

        df['municipio_id'] = df[['y', 'x']].apply(self.procesa_entidad, axis=1)

        df['ide_cp'] = df['ide_cp'].fillna(value=0).astype(int).astype(str)
        df['cve_diag_final'] = df['cve_diag_final'].astype(int)

        gdf = gpd.GeoDataFrame(df[self.columnas], geometry=gpd.points_from_xy(df.y, df.x))
        # gdf = gdf[self.columnas]
        gdf.crs = 'EPSG:4326'
        # self.stdout.write(self.style.NOTICE('Insertando entidades'))

        gdf.to_postgis(Vector._meta.db_table, self.engine, if_exists="append", index=False)
        # print(gdf)

    def procesa_entidad(self, row):
        pp = Point(row[0], row[1], srid=4326)
        # print(pp.transform(3857, clone=True))
        mun = Municipio.objects.get(geometry__contains=pp)
        # print(mun)
        return mun.pk

    def handle(self, *args, **kwargs):
        archivo = kwargs['archivo']
        self.stdout.write(self.style.NOTICE('Cargando datos'))
        self.carga_datos(archivo)
