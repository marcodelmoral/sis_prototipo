from django.urls import path

from dengue.views import (
    AnalisisDengueAppView,
    ClusteringDengueAppView,
    SeriesDengueAppView,
    )

app_name = "dengue"

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
