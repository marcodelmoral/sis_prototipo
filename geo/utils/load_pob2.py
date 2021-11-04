import math
import multiprocessing as mp
import os
import time

import numpy as np
import pandas as pd


def procesa_totales(diccionario):
    for key, value in diccionario.items():
        if type(value) == str:
            try:
                diccionario[key] = int(value)
            except:
                diccionario[key] = None
        elif math.isnan(value):
            diccionario[key] = None

    return diccionario


def obtener_poblacion(carpeta):
    estados = []
    for subdir, dirs, files in os.walk(carpeta):
        for file in files:
            if file.endswith('.csv'):
                archivo = os.path.join(carpeta, file)
                estados.append(archivo)
    return estados


def cargar_poblacion(archivo):
    start_time = time.time()
    import django

    django.setup()
    from geo.models import Entidad, Municipio, Localidad, Manzana, Ageb

    df = pd.read_csv(archivo, dtype={'ENTIDAD': str, 'MUN': str, 'LOC': str, 'AGEB': str, 'MZA': str}, )
    columnas = ["POBTOT", "POBFEM", "POBMAS"]
    df = df.replace('*', np.nan)
    entidad = Entidad.objects.filter(cve_ent=df['ENTIDAD'].iloc[0])
    df_entidad_totales = df[df['NOM_LOC'].str.contains('total de la entidad', regex=False, case=False, na=False)]
    totales_entidad = df_entidad_totales[columnas].to_dict('records')
    entidad.update(**procesa_totales(totales_entidad[0]))

    df_municipio_totales = df[df['NOM_LOC'].str.contains('total del municipio', regex=False, case=False, na=False)]
    for i, row in df_municipio_totales.iterrows():
        municipio = Municipio.objects.filter(cvegeo=f"{row['ENTIDAD'].zfill(2)}{row['MUN'].zfill(3)}")
        totales_municipio = row[columnas].to_dict()
        municipio.update(**procesa_totales(totales_municipio))

    df_localidades_totales = df[
        df['NOM_LOC'].str.contains('total de la localidad urbana', regex=False, case=False, na=False)
    ]
    for i, row in df_localidades_totales.iterrows():
        localidad = Localidad.objects.filter(
            cvegeo=f"{row['ENTIDAD'].zfill(2)}{row['MUN'].zfill(3)}{row['LOC'].zfill(4)}"
            )
        totales_localidad = row[columnas].to_dict()
        localidad.update(**procesa_totales(totales_localidad))

    df_ageb_totales = df[df['NOM_LOC'].str.contains('total ageb urbana', regex=False, case=False, na=False)]
    for i, row in df_ageb_totales.iterrows():
        cve_ageb = row['AGEB'].zfill(4) if row['AGEB'].isnumeric() else row['AGEB']
        ageb = Ageb.objects.filter(
            cvegeo=f"{row['ENTIDAD'].zfill(2)}{row['MUN'].zfill(3)}{row['LOC'].zfill(4)}{cve_ageb}"
            )
        totales_ageb = row[columnas].to_dict()
        ageb.update(**procesa_totales(totales_ageb))

    df_manzanas_totales = df[~df['NOM_LOC'].str.contains('total', regex=False, case=False, na=False)]
    for i, row in df_manzanas_totales.iterrows():
        cve_ageb = row['AGEB'].zfill(4) if row['AGEB'].isnumeric() else row['AGEB']
        manzana = Manzana.objects.filter(
            cvegeo=f"{row['ENTIDAD'].zfill(2)}{row['MUN'].zfill(3)}{row['LOC'].zfill(4)}{cve_ageb}{row['MZA'].zfill(3)}"
            )
        totales_manzana = row[columnas].to_dict()
        manzana.update(**procesa_totales(totales_manzana))

    final = time.time() - start_time
    return archivo, final


def paralelo_carga_poblacion(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    n = mp.cpu_count()
    print(f"Número de procesadores: {n}\n")
    pool = mp.Pool(n)
    poblacion = obtener_poblacion(carpeta)
    results = [pool.apply_async(cargar_poblacion, args=(i,)) for i in poblacion]
    pool.close()
    for ele in results:
        s = ele.get()
        print(f'Archivo: {s[0]}\nFinalizado en: {s[1]} segundos\n')
    print(f"Final: {time.ctime()}\n")
    final = time.time() - start_time
    print(f'Procesamiento en paralelo terminado en: {final} segundos')


def secuencial_carga_poblacion(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    poblacion = obtener_poblacion(carpeta)
    results = [cargar_poblacion(i) for i in poblacion]
    print(f"Final: {time.ctime()}\n")
    print(results)
    final = time.time() - start_time
    print(f'Procesamiento secuencial terminado en: {final} segundos')


def carga_poblacion(carpeta='INEGI/poblacion/censo2020/resultados', paralelo=True):
    if paralelo:
        paralelo_carga_poblacion(carpeta)
    else:
        secuencial_carga_poblacion(carpeta)


if __name__ == "__main__":
    carga_poblacion()
