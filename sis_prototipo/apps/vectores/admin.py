from django.contrib import admin

from sis_prototipo.apps.vectores.models import DatosAgregados, Vector

admin.site.register(Vector)
admin.site.register(DatosAgregados)
