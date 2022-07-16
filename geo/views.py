from django.views.generic import TemplateView
from rest_framework.generics import ListAPIView

from geo.models import Entidad
from geo.serializers import EntidadSerializer


class EntidadListView(ListAPIView):
    queryset = Entidad.objects.all()
    serializer_class = EntidadSerializer


class ExploracionAppView(TemplateView):
    template_name = "geo/exploracion.html"
