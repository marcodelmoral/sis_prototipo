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
    from geo.models import Entidad

    df = pd.read_csv(archivo, dtype={'ENTIDAD': str, 'MUN': str, 'LOC': str, 'AGEB': str, 'MZA': str}, )
    columnas = ["POBTOT", "POBFEM", "POBMAS"]
    df = df.replace('*', np.nan)
    entidad = Entidad.objects.filter(cve_ent=df['ENTIDAD'].iloc[0])
    df_entidad_totales = df[df['NOM_LOC'].str.contains('total de la entidad', regex=False, case=False, na=False)]
    totales_entidad = df_entidad_totales[columnas].to_dict('records')
    entidad.update(**procesa_totales(totales_entidad[0]))

    df_municipio_totales = df[df['NOM_LOC'].str.contains('total del municipio', regex=False, case=False, na=False)]
    for i, row in df_municipio_totales.iterrows():
        entidad = Entidad.objects.get(cve_ent=row['ENTIDAD'].zfill(2))
        municipio = entidad.municipio_set.filter(cve_mun=str(row['MUN'].zfill(3)))
        totales_municipio = row[columnas].to_dict()
        municipio.update(**procesa_totales(totales_municipio))

    df_localidades_totales = df[
        df['NOM_LOC'].str.contains('total de la localidad urbana', regex=False, case=False, na=False)
    ]
    for i, row in df_localidades_totales.iterrows():
        entidad = Entidad.objects.get(cve_ent=row['ENTIDAD'].zfill(2))
        municipio = entidad.municipio_set.get(cve_mun=str(row['MUN'].zfill(3)))
        localidad = municipio.localidad_set.filter(cve_loc=str(row['LOC'].zfill(4)))
        totales_localidad = row[columnas].to_dict()
        localidad.update(**procesa_totales(totales_localidad))

    df_agebu_totales = df[df['NOM_LOC'].str.contains('total ageb urbana', regex=False, case=False, na=False)]
    for i, row in df_agebu_totales.iterrows():
        entidad = Entidad.objects.get(cve_ent=row['ENTIDAD'].zfill(2))
        municipio = entidad.municipio_set.get(cve_mun=str(row['MUN'].zfill(3)))
        # No existe San Jose Vieno en BJS 2047
        try:
            print(row['ENTIDAD'], row["LOC"])
            localidad = municipio.localidad_set.get(cve_loc=str(row['LOC'].zfill(4)))
            agebu = localidad.agebs.filter(cve_ageb=str(row['AGEB']))
            totales_agebu = row[columnas].to_dict()
            agebu.update(**procesa_totales(totales_agebu))
        except Exception as e:
            print(e)
            pass

    df_manzanas_totales = df[~df['NOM_LOC'].str.contains('total', regex=False, case=False, na=False)]
    for i, row in df_manzanas_totales.iterrows():
        entidad = Entidad.objects.get(cve_ent=df['ENTIDAD'].iloc[0])
        municipio = entidad.municipio_set.get(cve_mun=str(row['MUN'].zfill(3)))
        try:
            localidad = municipio.localidad_set.get(cve_loc=str(row['LOC'].zfill(4)))
            # En aguascalientes no hay ageb 1301 para mun 01 loc 001
            try:
                ageb = localidad.ageb_set.get(cve_ageb=str(row['AGEB']))
            except:
                try:
                    ageb = municipio.ageb_set.get(cve_ageb=str(row['AGEB']))
                except:
                    pass
            manzana = ageb.manzana_set.filter(cve_mza=str(row['MZA']))
            totales_manzana = row[columnas].to_dict()
            manzana.update(**procesa_totales(totales_manzana))
        except:
            pass
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


def carga_poblacion(carpeta='INEGI/poblacion/censo2020/resultados', paralelo=False):
    if paralelo:
        paralelo_carga_poblacion(carpeta)
    else:
        secuencial_carga_poblacion(carpeta)


if __name__ == "__main__":
    carga_poblacion()
