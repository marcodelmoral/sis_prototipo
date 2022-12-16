from django.urls import path

from prototipo.apps.vectores.views import (
    AnalisisDengueAppView,
    ClusteringDengueAppView,
    SeriesDengueAppView,
)

app_name = "vectores"

urlpatterns = [
    path(
        "analisis_dengue",
        AnalisisDengueAppView.as_view(),
        name="analisis_dengue",
    ),
    path(
        "clustering_dengue",
        ClusteringDengueAppView.as_view(),
        name="clustering_dengue",
    ),
    path(
        "tablero_dengue",
        SeriesDengueAppView.as_view(),
        name="series_dengue",
    ),
]
