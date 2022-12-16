from rest_framework import viewsets

from prototipo.apps.geo.models import Entidad, Localidad, Manzana, Municipio
from prototipo.apps.geo.serializers import EntidadGeoSerializer, LocalidadGeoSerializer, ManzanaGeoSerializer, \
    MunicipioGeoSerializer


class EntidadGeoViewSet(viewsets.ModelViewSet):
    queryset = Entidad.objects.all()
    serializer_class = EntidadGeoSerializer
    http_method_names = ['get']


class MunicipioGeoViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioGeoSerializer
    http_method_names = ['get']


class LocalidadGeoViewSet(viewsets.ModelViewSet):
    queryset = Localidad.objects.all()
    serializer_class = LocalidadGeoSerializer
    http_method_names = ['get']


class ManzanaGeoViewSet(viewsets.ModelViewSet):
    queryset = Manzana.objects.all()
    serializer_class = ManzanaGeoSerializer
    http_method_names = ['get']
