import glob
import multiprocessing as mp
import time

from django.contrib.gis.utils import LayerMapping


# TODO: revisar porque no carga San Quintin de Baja California


def cargar_geojson(archivo):
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

    print("Guardando entidad")
    lment = LayerMapping(Entidad, f"{archivo}/entidad.geojson", entidad_mapping, transform=True, encoding='utf-8')
    lment.save(strict=True, verbose=True)
    print("Guardando municipio")
    lmmun = LayerMapping(
        Municipio, f"{archivo}/municipios.geojson", municipio_mapping, transform=True, encoding='utf-8'
        )
    lmmun.save(strict=True, verbose=True)
    print("Guardando localidad")
    lml = LayerMapping(
        Localidad, f"{archivo}/localidades.geojson", localidad_mapping, transform=True, encoding='utf-8'
        )
    lml.save(strict=True, verbose=True)
    print("Guardando ageb urbano")
    lmau = LayerMapping(Ageb, f"{archivo}/agebs_urbanos.geojson", ageb_mapping, transform=True, encoding='utf-8')
    lmau.save(strict=True, verbose=True)
    print("Guardando ageb rural")
    lmar = LayerMapping(Ageb, f"{archivo}/agebs_rurales.geojson", ageb_mapping, transform=True, encoding='utf-8')
    lmar.save(strict=True, verbose=True)
    print("Guardando manzana")
    lme = LayerMapping(Manzana, f"{archivo}/manzanas.geojson", manzana_mapping, transform=True, encoding='utf-8')
    lme.save(strict=True, verbose=True)

    final = time.time() - start_time
    return archivo, final


def paralelo_carga_geojson(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    n = mp.cpu_count()
    print(f"Número de procesadores: {n}\n")
    pool = mp.Pool(n)
    estados = glob.glob('INEGI/geojsons/*')
    results = [pool.apply_async(cargar_geojson, args=(i,)) for i in estados]
    pool.close()
    for ele in results:
        s = ele.get()
        print(f'Archivo: {s[0]}\nFinalizado en: {s[1] / 60} minutos\n')
    print(f"Final: {time.ctime()}\n")
    final = time.time() - start_time
    print(f'Procesamiento en paralelo terminado en: {final / 60} minutos')


def secuencial_carga_geojson(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    print(f"Procesando: {carpeta}")
    estados = glob.glob('INEGI/geojsons/*')
    results = [cargar_geojson(i) for i in estados]
    print(f"Final: {time.ctime()}\n")
    print(results)
    final = time.time() - start_time
    print(f'Procesamiento secuencial terminado en: {final / 60} minutos')


def carga_geojson(carpeta='INEGI/geojsons', paralelo=True):
    if paralelo:
        paralelo_carga_geojson(carpeta)
    else:
        secuencial_carga_geojson(carpeta)


if __name__ == "__main__":
    carga_geojson()
