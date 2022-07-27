from rest_framework import viewsets

from geo.models import Entidad
from geo.serializers import EntidadGeoSerializer


class EntidadGeoViewSet(viewsets.ModelViewSet):
    queryset = Entidad.objects.all()
    serializer_class = EntidadGeoSerializer
    http_method_names = ['get']
