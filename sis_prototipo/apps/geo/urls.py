from django.urls import path

from sis_prototipo.apps.geo.views import ExploracionAppView

app_name = "geo"

urlpatterns = [
    path("exploracion", ExploracionAppView.as_view(), name="exploracion"),
]
