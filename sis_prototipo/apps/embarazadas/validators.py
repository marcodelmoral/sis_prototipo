import pandas as pd
import os
from django.conf import settings
from django.core.exceptions import ValidationError
from os.path import splitext
import re
import datetime



def validador_nss(value):
    try:
        int(value)
    except ValueError:
        raise ValidationError('NSS no válido: No debe contener letras')

    if len(value) != 11:
        raise ValidationError('NSS no válido: Debe contener exactamente 11 números')


# def validador_nss(value):
#     regex = r"^(\d{2})(\d{2})(\d{2})\d{5}$"
#     validado = re.match(regex, value)
#     if not validado:
#         raise ValidationError('Deben ser 11 dígitos y no contener letra alguna')
#     sub = int(validado.group(1))
#     year = datetime.datetime.now().year
#     alta = int(validado.group(2))
#     nac = int(validado.group(3))
#
#     if sub != 97:
#         if alta <= year:
#             alta += 100
#         if nac <= year:
#             nac += 100
#         if nac > alta:
#             raise ValidationError('NSS inválido')
#
#     if not luhn(value):
#         raise ValidationError('NSS inválido')


def validador_archivo_embarazada(value):
    ext = splitext(value.name)[1][1:].lower()
    if str(ext) != 'xlsx':
        raise ValidationError('Debe ser un archivo de Excel .xlsx')
    try:
        datos = pd.read_excel(value,
                              encoding='latin-1',
                              low_memory=False,
                              dtype=object,
                              usecols=settings.COLUMNAS_EMBARAZADA,
                              skiprows=1)
        if not set(datos.columns) <= set(settings.COLUMNAS_EMBARAZADA):
            raise ValidationError('Las columnas del archivo son incorrectas')
    except Exception as e:
        raise ValidationError(f'El contenido del archivo no es válido, error {e}')


def validador_cp(value):
    if len(str(value)) != 5:
        raise ValidationError('Código Postal no válido')
    try:
        int(value)
    except ValueError:
        raise ValidationError('Código Postal no válido')
