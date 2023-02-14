from django.views.generic import TemplateView

from sis_prototipo.apps.geo.models import Entidad
from sis_prototipo.apps.vectores.dash_apps import (
    analisis_dengue,
    clustering_dengue,
    series_dengue
)
from sis_prototipo.apps.vectores.dash_apps.utils import entidades_opciones_dropdown


class DashAppView(TemplateView):
    template_name = "vectores/aplicacion_dash.html"
    dash_app = None
    titulo = None

    def get_context_data(self, **kwargs):
        context = super(DashAppView, self).get_context_data(**kwargs)
        context["dash_app"] = self.dash_app.nombre
        context["titulo"] = self.titulo
        return context


class AnalisisDengueAppView(DashAppView):
    dash_app = analisis_dengue
    titulo = "Análisis de datos"


class ClusteringDengueAppView(DashAppView):
    dash_app = clustering_dengue
    titulo = "Clustering de Dengue"


class SeriesDengueAppView(DashAppView):
    dash_app = series_dengue
    titulo = "Análisis de series de tiempo"
