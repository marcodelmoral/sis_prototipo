from os.path import splitext

import pandas as pd
from django.conf import settings
from django.core.exceptions import ValidationError


def validador_archivo_sinave(value):
    ext = splitext(value.name)[1][1:].lower()
    if str(ext) != 'txt':
        raise ValidationError('Debe ser un archivo .txt')
    try:
        datos = pd.read_csv(value, sep='|',
                            encoding='latin-1',
                            low_memory=False,
                            dtype=object,
                            usecols=settings.COLUMNAS_VECTOR)
    except Exception as e:
        raise ValidationError(f'El contenido del archivo no es válido, error: {e}')

    if not set(datos.columns) <= set(settings.COLUMNAS_VECTOR):
        raise ValidationError('Las columnas del archivo son incorrectas')


# todo validador de estudio epidemiologico
def validador_archivo_estudio(value):
    ext = splitext(value.name)[1][1:].lower()
    if str(ext) != 'xlsx' or str(ext) != 'xls':
        raise ValidationError('Debe ser un archivo de Excel .xlsx')
