from django.contrib import admin
from sis_prototipo.apps.embarazadas.models import Embarazada, ArchivoEmbarazada
from leaflet.admin import LeafletGeoAdminMixin
from simple_history.admin import SimpleHistoryAdmin


class LeafletSimple(LeafletGeoAdminMixin, SimpleHistoryAdmin):
    pass


admin.site.register(Embarazada, LeafletSimple)
admin.site.register(ArchivoEmbarazada)



