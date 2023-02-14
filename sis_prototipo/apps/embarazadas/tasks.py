from celery import task, shared_task
import os
from django.core.mail import send_mail
from celery.utils.log import get_task_logger
from django.conf import settings
from datetime import date, timedelta
from django.conf import settings
from django.db.models import F, Case, When

from django.db import transaction
import sys

from sis_prototipo.apps.embarazadas.models import Embarazada

logger = get_task_logger(__name__)


# todo geocodificar imprecisos y hacer calculo de relaciones
@task()
def diario():
    # Desactiva si han pasado n dias
    embarazada_delta = date.today() - timedelta(days=settings.MANTENER_EMBARAZADA)
    Embarazada.objects.activos().update(ACTIVO=Case(When(FECHA_PARTO__lte=embarazada_delta, then=False)))

    vector_delta = date.today() - timedelta(days=settings.MANTENER_VECTOR)
    Vector.objects.activos().update(ACTIVO=Case(When(FECHA_SOL_ATEN__lte=vector_delta, then=False)))

    # Cuando las semanas de gestacion son iguales a 37
    Embarazada.objects.activos().update(PROBABLE_PARTO=Case(When(sdg__exact=37, then=True)))

    # Me quedo bien guapo: selecciona activos, con probable parto y que aun no se ha avisado y manda correo
    Embarazada.objects.activos().probable_parto().sin_avisar().mandar_correo()


@shared_task
def proceso_asinc_epidemio(entrada):
    datos = aplica_preprocesa(entrada)
    try:
        datos['archivo_epidemio'] = ArchivoEpidemio.objects.get(pk=datos['archivo_epidemio'])
    except:
        datos['archivo_epidemio'] = None
    try:
        datos['DES_EDO_RES'] = Entidad.objects.get(nomgeo__icontains=datos['DES_EDO_RES'])
    except:
        datos['DES_EDO_RES'] = None
    try:
        datos['DES_MPO_RES'] = datos.get('DES_EDO_RES').municipio_set.get(nomgeo__icontains=datos['DES_MPO_RES'])
    except:
        datos['DES_MPO_RES'] = None
    try:
        datos['DES_LOC_RES'] = datos.get('DES_MPO_RES').localidad_set.get(nomloc__icontains=datos['DES_LOC_RES'])
    except:
        datos['DES_LOC_RES'] = None
    modelo = Vector(**datos)
    modelo.save()
    logger.info("Finalizando")


@shared_task
def proceso_asinc_embarazada(entrada):
    datos = aplica_preprocesa(entrada)

    try:
        if datos['DES_EDO_RES'] == 'DISTRITO FEDERAL':
            datos['DES_EDO_RES'] = Entidad.objects.get(nomgeo__icontains='Ciudad de Mexico')
        datos['DES_EDO_RES'] = Entidad.objects.get(nomgeo__icontains=datos['DES_EDO_RES'])
    except:
        datos['DES_EDO_RES'] = None
    try:
        datos['DES_MPO_RES'] = datos.get('DES_EDO_RES').municipio_set.get(nomgeo__icontains=datos['DES_MPO_RES'])
    except:
        datos['DES_MPO_RES'] = None
    try:
        datos['DES_LOC_RES'] = datos.get('DES_MPO_RES').localidad_set.get(nomloc__icontains=datos['DES_LOC_RES'])
    except:
        datos['DES_LOC_RES'] = None
    modelo = Embarazada(**datos)
    modelo.save()
    logger.info("Finalizando")


@shared_task
def proceso_asinc_sinave(entrada, pk):
    datos = aplica_preprocesa(entrada)

    datos.update({'archivo_sinave':  ArchivoVector.objects.get(pk=pk)})

    try:
        datos['DES_EDO_RES'] = Entidad.objects.get(cve_ent=datos.get('CVE_EDO_RES').zfill(2))
    except:
        datos['DES_EDO_RES'] = None

    try:
        datos['DES_MPO_RES'] = datos.get('DES_EDO_RES').municipio_set.get(cve_mun=datos.get('CVE_MPO_RES').zfill(3))
    except:
        datos['DES_MPO_RES'] = None

    try:
        datos['DES_LOC_RES'] = datos.get('DES_MPO_RES').localidad_set.get(cve_loc=datos.get('CVE_LOC_RES').zfill(4))
    except:
        datos['DES_LOC_RES'] = None

    datos.pop('CVE_EDO_RES', None)
    datos.pop('CVE_MPO_RES', None)
    datos.pop('CVE_LOC_RES', None)

    modelo = Vector(**datos)
    modelo.save()
    logger.warning("Finalizando")
