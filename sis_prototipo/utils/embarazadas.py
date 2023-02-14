
import pandas as pd
from django.conf import settings


# from django.db import transaction
#
# from sis_prototipo.apps.embarazadas.models import Embarazada
# from sis_prototipo.apps.geo.models import Entidad


def preprocesa_excel_embarazada(archivo):
    """
        Regresa una tupla, cuyo primer elemento es el dataframe preprocesado
        y el segundo elemento es el tamano del dataframe
    """
    file = pd.ExcelFile(archivo, engine='xlrd')
    df = {}
    for fila in file.sheet_names:
        df[fila] = pd.read_excel(file,
                                 sheet_name=fila,
                                 encoding='latin-1',
                                 dtypes=object,
                                 skiprows=1)

    datos = pd.concat(list(df.values()))

    datos = datos[settings.COLUMNAS_EMBARAZADA]
    datos = datos.fillna('')
    datos.columns = settings.COLUMNAS_EMBARAZADA_BD
    return datos.to_dict('records')





# def aplica_preprocesa_embarazada(entrada, pk_usuario):
#     excel_embarazada = preprocesa_excel_embarazada(entrada)
#     datos = aplica_preprocesa(excel_embarazada)
#     usuario = User.objects.get(pk=pk_usuario)
#
#     with transaction.atomic():
#         for elemento in datos:
#             elemento.update({'UMF': usuario.umf})
#             elemento['DES_EDO_RES'] = Entidad.objects.get(nomgeo__icontains=elemento.get('DES_EDO_RES'))
#             elemento['DES_MPO_RES'] = elemento.get('DES_EDO_RES').municipio_set.get(nomgeo__icontains=elemento.get('DES_MPO_RES'))
#             elemento['DES_LOC_RES'] = elemento.get('DES_MPO_RES').localidad_set.get(nomloc__icontains=elemento.get('DES_LOC_RES'))
#             modelo = Embarazada(**elemento)
#             modelo.save()
