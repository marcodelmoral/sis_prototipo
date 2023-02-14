from django.db.models.signals import post_save
from django.conf import settings
from geo.funciones import preprocesa_csv_vectores, preprocesa_excel_embarazada, preprocesa_excel_vectores
import os
from celery import group
from geo.tasks import proceso_asinc_sinave, proceso_asinc_embarazada, proceso_asinc_epidemio
from geo.models import ArchivoVector, ArchivoEmbarazada, ArchivoEpidemio


def sinave_post_save(sender, instance, signal, *args, **kwargs):
    archivo = instance
    archivo_path = archivo.archivo.path
    filename = os.path.basename(archivo_path)
    file_name = os.path.join('MEDIA', filename)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    lista = preprocesa_csv_vectores(file_path)
    jobs = group(proceso_asinc_sinave.s(ele, instance.pk) for ele in lista)
    jobs.apply_async()


post_save.connect(sinave_post_save, sender=ArchivoVector)


def excel_post_save(sender, instance, signal, *args, **kwargs):
    archivo = instance
    archivo_path = archivo.archivo.path
    filename = os.path.basename(archivo_path)
    file_name = os.path.join('MEDIA', filename)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    lista = preprocesa_excel_embarazada(file_path)
    jobs = group(proceso_asinc_embarazada.s(item) for item in lista)
    jobs.apply_async()


post_save.connect(excel_post_save, sender=ArchivoEmbarazada)


def epidemio_post_save(sender, instance, signal, *args, **kwargs):
    archivo = instance
    archivo_path = archivo.archivo.path
    filename = os.path.basename(archivo_path)
    file_name = os.path.join('MEDIA', filename)
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    lista = preprocesa_excel_vectores(file_path)
    for item in lista:
        item.update({'archivo': instance.pk})
    jobs = group(proceso_asinc_epidemio.s(item) for item in lista)
    jobs.apply_async()


post_save.connect(epidemio_post_save, sender=ArchivoEpidemio)
