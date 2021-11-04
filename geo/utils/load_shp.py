import multiprocessing as mp
import os
import re
import time

from django.contrib.gis.utils import LayerMapping


# TODO: revisar porque no carga San Quintin de Baja California


def obtener_estados(carpeta):
    estados = []
    for estado in os.listdir(carpeta):
        if 'zip' not in estado:
            estado_folder = os.path.join(carpeta, estado)
            for datos in os.listdir(estado_folder):
                if 'conjunto_de_datos' in datos:
                    datos_folder = os.path.join(estado_folder, datos)
                    estados.append(datos_folder)
    return estados


def cargar_shp(archivo):
    start_time = time.time()
    import django

    django.setup()
    from geo.models import (
        Entidad,
        Municipio,
        Localidad,
        Ageb,
        Manzana,
        entidad_mapping,
        municipio_mapping,
        localidad_mapping,
        ageb_mapping,
        manzana_mapping,
        )

    entidad = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(ent).shp\b', f)][0]
    municipio = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(mun).shp\b', f)][0]
    agebu = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(' r'a_procesado).geojson\b', f)][0]
    agebr = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(' r'ar_procesado).geojson\b', f)][0]
    localidad = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(' r'l_procesado).geojson\b', f)][0]

    lpr = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(' r'lpr_procesado).geojson\b', f)][0]
    manzana = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(' r'm_procesado).geojson\b', f)][0]
    # serv = [ele for ele in
    #             os.listdir(archivo) if 'serv.shp' in ele][0]
    print("Guardando entidad")
    lment = LayerMapping(Entidad, os.path.join(archivo, entidad), entidad_mapping, transform=True, encoding='utf-8')
    lment.save(strict=True, verbose=True)
    print("Guardando municipio")
    lmmun = LayerMapping(
        Municipio, os.path.join(archivo, municipio), municipio_mapping, transform=True, encoding='utf-8'
        )
    lmmun.save(strict=True, verbose=True)
    print("Guardando localidad")
    lml = LayerMapping(
        Localidad, os.path.join(archivo, localidad), localidad_mapping, transform=True, encoding='utf-8'
        )
    lml.save(strict=True, verbose=True)
    print("Guardando ageb urbano")
    lmau = LayerMapping(Ageb, os.path.join(archivo, agebu), ageb_mapping, transform=True, encoding='utf-8')
    lmau.save(strict=True, verbose=True)
    print("Guardando ageb rural")
    lmar = LayerMapping(Ageb, os.path.join(archivo, agebr), ageb_mapping, transform=True, encoding='utf-8')
    lmar.save(strict=True, verbose=True)
    # print("Guardando localidad puntual")
    # lmpr = LayerMapping(Localidad, os.path.join(archivo, lpr), localidad_mapping, transform=True, encoding='utf-8')
    # lmpr.save(strict=True, verbose=True)
    print("Guardando manzana")
    lme = LayerMapping(Manzana, os.path.join(archivo, manzana), manzana_mapping, transform=True, encoding='utf-8')
    lme.save(strict=True, verbose=True)

    # lmserv = LayerMapping(Servicio, os.path.join(archivo, serv),
    #                       servicio_mapping,
    #                       transform=True, encoding='utf-8')
    # lmserv.save(strict=True, verbose=True)

    final = time.time() - start_time
    return archivo, final


def paralelo_carga_shp(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    n = mp.cpu_count()
    print(f"Número de procesadores: {n}\n")
    pool = mp.Pool(n)
    estados = os.listdir(carpeta)
    results = [pool.apply_async(cargar_shp, args=(i,)) for i in estados]
    pool.close()
    for ele in results:
        s = ele.get()
        print(f'Archivo: {s[0]}\nFinalizado en: {s[1] / 60} minutos\n')
    print(f"Final: {time.ctime()}\n")
    final = time.time() - start_time
    print(f'Procesamiento en paralelo terminado en: {final / 60} minutos')


def secuencial_carga_shp(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    print(f"Procesando: {carpeta}")
    estados = obtener_estados(carpeta)
    results = [cargar_shp(i) for i in estados]
    print(f"Final: {time.ctime()}\n")
    print(results)
    final = time.time() - start_time
    print(f'Procesamiento secuencial terminado en: {final / 60} minutos')


def carga_shp(carpeta='INEGI/geojsons', paralelo=True):
    if paralelo:
        paralelo_carga_shp(carpeta)
    else:
        secuencial_carga_shp(carpeta)


if __name__ == "__main__":
    carga_shp()
