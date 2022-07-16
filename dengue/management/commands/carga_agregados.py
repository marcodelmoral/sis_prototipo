import time
import warnings

import pandas as pd
from django.conf import settings
from django.core.management import BaseCommand
from sqlalchemy import create_engine

from dengue.models import DatosAgregados, Vector

warnings.simplefilter(action="ignore", category=FutureWarning)


class Command(BaseCommand):
    help = "Carga series de tiempo de dengue y clima"

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.map_diagnostico = dict((y, x) for x, y in Vector.DIAGNOSTICO)
        self.entidades_map = {
            "Aguascalientes": "01",
            "Baja California": "02",
            "Baja California Sur": "03",
            "Campeche": "04",
            "Coahuila": "05",
            "Colima": "06",
            "Chiapas": "07",
            "Chihuahua": "08",
            "Distrito Federal": "09",
            "Durango": "10",
            "Guanajuato": "11",
            "Guerrero": "12",
            "Hidalgo": "13",
            "Jalisco": "14",
            "México": "15",
            "Michoacán": "16",
            "Morelos": "17",
            "Nayarit": "18",
            "Nuevo León": "19",
            "Oaxaca": "20",
            "Puebla": "21",
            "Querétaro": "22",
            "Quintana Roo": "23",
            "San Luis Potosí": "24",
            "Sinaloa": "25",
            "Sonora": "26",
            "Tabasco": "27",
            "Tamaulipas": "28",
            "Tlaxcala": "29",
            "Veracruz": "30",
            "Yucatán": "31",
            "Zacatecas": "32",
            }
        self.columnas_map = {
            "Fecha": "fecha",
            "Casos": 1,
            "Precip": 5,
            "Tmax": 3,
            "Tmed": 4,
            "Tmin": 2,
            "index": "id",
            }
        username = settings.DATABASES["default"]["USER"]
        password = settings.DATABASES["default"]["PASSWORD"]
        host = settings.DATABASES["default"]["HOST"]
        database = settings.DATABASES["default"]["NAME"]

        db_uri = f"postgresql://{username}:{password}@{host}:5432/{database}"

        self.engine = create_engine(db_uri).connect()

    def add_arguments(self, parser):
        parser.add_argument("archivo", nargs="?", type=str, help="Archivo de datos agregados",
                            default="data/agregados/serie_final.csv")

    def carga_datos(self, archivo):
        df = pd.read_csv(archivo, index_col=None, low_memory=False, encoding="latin-1")
        df.reset_index(inplace=True)
        df["entidad_id"] = df["Entidad"].map(self.entidades_map)
        df.drop(columns="Entidad", inplace=True)
        df.rename(columns=self.columnas_map, inplace=True)
        df = df.melt(id_vars=['fecha', 'entidad_id'], value_vars=[1, 2, 3, 4, 5])
        df = df.reset_index()
        df.rename(columns={'index': 'id', 'variable': 'tipo', 'value': 'valor'}, inplace=True)
        df.to_sql(
            DatosAgregados._meta.db_table,
            if_exists="append",
            index=False,
            con=self.engine,
            )

    def handle(self, *args, **kwargs):
        archivo = kwargs["archivo"]
        self.stdout.write(self.style.WARNING("Cargando datos agregados"))
        start_time = time.time()
        self.carga_datos(archivo)
        tiempo = (time.time() - start_time) / 60
        self.stdout.write(
            self.style.SUCCESS(f"Tiempo transcurrido: {tiempo:.3f} minutos")
            )
