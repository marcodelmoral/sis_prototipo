from rest_framework import viewsets
from rest_framework_gis.filterset import GeoFilterSet

from prototipo.apps.vectores.models import Vector
from prototipo.apps.vectores.serializers import VectorSerializer


class VectorFilter(GeoFilterSet):
    # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Vector
        fields = ['municipio', 'cve_diag_final']


class VectorViewSet(viewsets.ModelViewSet):
    serializer_class = VectorSerializer
    queryset = Vector.objects.all()
    # filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VectorFilter
