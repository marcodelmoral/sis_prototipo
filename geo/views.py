from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView

from geo.models import Entidad
from geo.serializers import EntidadGeoSerializer


class EntidadListView(ListAPIView):
    queryset = Entidad.objects.all()
    serializer_class = EntidadGeoSerializer


class ExploracionAppView(TemplateView):
    template_name = "geo/exploracion.html"
