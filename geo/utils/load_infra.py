import math
import multiprocessing as mp
import os
import time

from simpledbf import Dbf5


def obtener_infraestructura(carpeta):
    estados = []
    for subdir, dirs, files in os.walk(carpeta):
        for file in files:
            if file.endswith('.DBF'):
                archivo = os.path.join(carpeta, file)
                estados.append(archivo)
    return estados


def procesa_columnas(columna):
    if columna.endswith('_'):
        return columna[:-1]
    else:
        return columna


def procesa_totales(diccionario):
    for key, value in diccionario.items():
        if type(value) == str:
            diccionario[key] = int(value)
        elif math.isnan(value):
            diccionario[key] = None

    return diccionario


def cargar_infraestructura(archivo):
    start_time = time.time()
    import django
    django.setup()
    from geo.models import Entidad
    dbf = Dbf5(archivo, codec='latin-1')
    df = dbf.to_dataframe()
    df.columns = [procesa_columnas(col) for col in df.columns]
    columnas = list(df.columns)[8:-1]
    for i, row in df.iterrows():
        entidad = Entidad.objects.get(cve_ent=str(row['ENT']))
        municipio = entidad.municipio_set.get(cve_mun=str(row['MUN']))

        try:
            localidad = municipio.localidad_set.get(cve_loc=str(
                row['LOC']))
            # En aguascalientes no hay ageb 1301 para mun 01 loc 001
            try:
                ageb = municipio.ageb_set.get(cve_ageb=str(
                    row['AGEB']))
            except:
                try:
                    ageb = municipio.agebr_set.get(cve_ageb=str(
                        row['AGEB']))
                except:
                    pass
            manzana = ageb.manzana_set.filter(cve_mza=str(row['MZA']))
            totales_manzana = row[columnas].to_dict()
            manzana.update(**procesa_totales(totales_manzana))
        except:
            pass
    final = time.time() - start_time
    return archivo, final


def paralelo_carga_infraestructura(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    n = mp.cpu_count()
    print(f"Número de procesadores: {n}\n")
    pool = mp.Pool(n)
    infraestructura = obtener_infraestructura(carpeta)
    results = [pool.apply_async(cargar_infraestructura, args=(i,)) for i in
               infraestructura]
    pool.close()
    for ele in results:
        s = ele.get()
        print(f'Archivo: {s[0]}\nFinalizado en: {s[1]} segundos\n')
    print(f"Final: {time.ctime()}\n")
    final = time.time() - start_time
    print(f'Procesamiento en paralelo terminado en: {final} segundos')


def secuencial_carga_infraestructura(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    infraestructura = obtener_infraestructura(carpeta)
    results = [cargar_infraestructura(i) for i in infraestructura]
    print(f"Final: {time.ctime()}\n")
    print(results)
    final = time.time() - start_time
    print(f'Procesamiento secuencial terminado en: {final} segundos')


def carga_infraestructura(carpeta='data/infraestructura', paralelo=True):
    if paralelo:
        paralelo_carga_infraestructura(carpeta)
    else:
        secuencial_carga_infraestructura(carpeta)


if __name__ == "__main__":
    carga_infraestructura()
