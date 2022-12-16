from django.contrib import admin

from prototipo.apps.vectores.models import DatosAgregados, Vector

admin.site.register(Vector)
admin.site.register(DatosAgregados)
