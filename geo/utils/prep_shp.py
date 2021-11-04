import multiprocessing as mp
import os
import re
import time

import geopandas as gpd
from shapely.geometry import MultiPolygon, Polygon


# TODO: mejorar proceso de carga y procesamiento de datos
# TODO: cambiar todos as poligono simple, convertira a geojson
# TODO: Hacer otros ogrinspect


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


def procesa_shp(archivo):
    """
    # TODO: poner el campo centroide a los modelos de localidad
    # TODO: poner servicios
    Convertimos los puntos de localidad en un poligono cuyos lados son el mismo
    punto
    :param archivo:
    :return:
    """
    start_time = time.time()
    import django

    django.setup()
    from geo.models import Manzana, Localidad  # ,Servicio

    # map_fix = {
    #     "Área Verde": "Áreas Verdes",
    #     "Estación de Transporte Forán*": "Estación de Transporte Foráneo",
    #     "Observataorio Astronómico": "Observatorio Astronómico",
    # }
    # map_servicio = dict((y, x) for x, y in Servicio.SERVICIO_TIPO)
    # map_condicion = dict((y, x) for x, y in Servicio.CONDICION_TIPO)
    # map_geografico = dict((y, x) for x, y in Servicio.GEOGRAFICO_TIPO)
    map_ambito = dict((y, x) for x, y in Localidad.AMBITO_TIPO)
    map_tipo = dict((y, x) for x, y in Manzana.MANZANA_TIPO)
    map_plano = dict((y, x) for x, y in Localidad.PLANO_TIPO)

    localidad = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(' r'l).shp\b', f)][0]

    lpr = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(' r'lpr).shp\b', f)][0]

    agebu = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(' r'a).shp\b', f)][0]
    agebr = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(' r'ar).shp\b', f)][0]

    manzana = [f for f in os.listdir(archivo) if re.search(r'\b\d\d(' r'm).shp\b', f)][0]
    dfl = gpd.read_file(os.path.join(archivo, localidad), encoding='latin-1')
    # inconsistencia def inegi
    dfl["geometry"] = dfl["geometry"].apply(lambda x: MultiPolygon([x]) if x.geom_type == "Polygon" else x)

    dflpr = gpd.read_file(os.path.join(archivo, lpr), encoding='latin-1')
    dflpr['PLANO'] = dflpr.PLANO.map(map_plano).astype('int32')
    dflpr['AMBITO'] = 0
    dflpr['geometry'] = dflpr['geometry'].apply(
        lambda x: MultiPolygon([Polygon([(x.x, x.y), (x.x, x.y), (x.x, x.y), (x.x, x.y)])])
        )
    dfl['AMBITO'] = dfl.AMBITO.map(map_ambito).astype('int32')
    salida_localidadpr = lpr[:-4] + '_procesado.geojson'
    dflpr.to_file(os.path.join(archivo, salida_localidadpr), driver='GeoJSON', encoding='utf-8')
    salida_localidad = localidad[:-4] + '_procesado.geojson'
    dfl.to_file(os.path.join(archivo, salida_localidad), driver='GeoJSON', encoding='utf-8')

    dfu = gpd.read_file(os.path.join(archivo, agebu), encoding='latin-1')
    dfr = gpd.read_file(os.path.join(archivo, agebr), encoding='latin-1')
    dfu['AMBITO'] = 1
    dfr["CVE_LOC"] = ''
    dfr['AMBITO'] = 2
    salida_agebu = agebu[:-4] + '_procesado.geojson'
    salida_agebr = agebr[:-4] + '_procesado.geojson'

    dfu["geometry"] = dfu["geometry"].apply(lambda x: MultiPolygon([x]) if x.geom_type == "Polygon" else x)
    dfr["geometry"] = dfr["geometry"].apply(lambda x: MultiPolygon([x]) if x.geom_type == "Polygon" else x)

    dfu.to_file(os.path.join(archivo, salida_agebu), driver='GeoJSON', encoding='utf-8')
    dfr.to_file(os.path.join(archivo, salida_agebr), driver='GeoJSON', encoding='utf-8')

    dfm = gpd.read_file(os.path.join(archivo, manzana), encoding='latin-1')
    dfm['AMBITO'] = dfm.AMBITO.map(map_ambito).astype('int32')
    dfm['TIPOMZA'] = dfm.TIPOMZA.map(map_tipo).astype('int32')
    salida_manzana = manzana[:-4] + '_procesado.geojson'
    dfm.to_file(os.path.join(archivo, salida_manzana), driver='GeoJSON', encoding='utf-8')

    # sia_file = [ele for ele in
    #             os.listdir(archivo) if 'sia.shp' in ele][0]
    # sip_file = [ele for ele in
    #             os.listdir(archivo) if 'sip.shp' in ele][0]
    # dfa = gpd.read_file(os.path.join(archivo, sia_file),
    #                     codec='latin-1')
    # dfp = gpd.read_file(os.path.join(archivo, sip_file),
    #                     codec='latin-1')
    # num_estado = sia_file[:2]
    # dfa['AREA'] = dfa['geometry'].astype(str)
    # dfa['geometry'] = dfa['geometry'].centroid
    # dfp['AREA'] = None
    # df = dfp.append(dfa, sort=True)
    # df['TIPO'] = df.TIPO.replace(map_fix)
    # df['TIPO'] = df.TIPO.map(map_servicio).astype('int32')
    # df['CONDICION'] = df.CONDICION.map(map_condicion).astype('int32')
    # df['GEOGRAFICO'] = df.GEOGRAFICO.map(map_geografico).astype('int32')
    # df['AMBITO'] = df.AMBITO.map(map_ambito).astype('int32')

    #  df.to_file(os.path.join(archivo, f'{num_estado}serv.shp'))
    final = time.time() - start_time
    return archivo, final


def paralelo_preprocesa_shp(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    n = mp.cpu_count()
    print(f"Número de procesadores: {n}\n")
    pool = mp.Pool(n)
    estados = obtener_estados(carpeta)
    results = [pool.apply_async(procesa_shp, args=(i,)) for i in estados]

    pool.close()

    for ele in results:
        s = ele.get()
        print(f'Archivo: {s[0]}\nFinalizado en: {s[1] / 60} minutos\n')
    print(f"Final: {time.ctime()}\n")
    final = time.time() - start_time
    print(f'Procesamiento en paralelo terminado en: {final / 60} minutos')


def secuencial_preprocesa_shp(carpeta):
    start_time = time.time()
    print(f"Inicio : {time.ctime()}\n")
    estados = obtener_estados(carpeta)
    results = [procesa_shp(i) for i in estados]
    print(f"Final: {time.ctime()}\n")
    print(results)
    final = time.time() - start_time
    print(f'Procesamiento secuencial terminado en: {final / 60} minutos')


def preprocesa_shp(carpeta='INEGI/marco', paralelo=True):
    if paralelo:
        paralelo_preprocesa_shp(carpeta)
    else:
        secuencial_preprocesa_shp(carpeta)


if __name__ == "__main__":
    preprocesa_shp()
