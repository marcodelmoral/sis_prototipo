from django.views.generic import TemplateView

# noinspection PyUnresolvedReferences
from dengue.dash_apps import (
    analisis_dengue,
    clustering_dengue,
    series_dengue,
    )


class DashAppView(TemplateView):
    template_name = "dengue/aplicacion_dash.html"
    dash_app = None
    titulo = None

    def get_context_data(self, **kwargs):
        context = super(DashAppView, self).get_context_data(**kwargs)
        context["dash_app"] = self.dash_app.nombre
        context["titulo"] = self.titulo
        return context


class AnalisisDengueAppView(DashAppView):
    dash_app = analisis_dengue
    titulo = "Analisis de datos"


class ClusteringDengueAppView(DashAppView):
    dash_app = clustering_dengue
    titulo = "Clustering de Dengue"


class SeriesDengueAppView(DashAppView):
    dash_app = series_dengue
    titulo = "Tablero de datos"

# class SeriesAppView(DashAppView):
#     dash_app = clustering_dengue
#     titulo = "Clustering de Dengue"
