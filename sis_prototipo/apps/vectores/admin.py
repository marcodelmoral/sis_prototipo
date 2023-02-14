from django.contrib import admin
from sis_prototipo.apps.vectores.models import DatosAgregados, Vector
from leaflet.admin import LeafletGeoAdminMixin
from simple_history.admin import SimpleHistoryAdmin

class LeafletSimple(LeafletGeoAdminMixin, SimpleHistoryAdmin):
    pass


admin.site.register(Vector, LeafletSimple)
admin.site.register(DatosAgregados)
