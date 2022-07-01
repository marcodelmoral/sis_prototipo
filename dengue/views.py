from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework_gis.filterset import GeoFilterSet

from dengue.models import Vector
from dengue.serializers import VectorSerializer


class VectorFilter(GeoFilterSet):
    # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Vector
        fields = ['municipio', 'des_diag_final']


class VectorViewSet(viewsets.ModelViewSet):
    serializer_class = VectorSerializer
    queryset = Vector.objects.all()
    # filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VectorFilter


class SeriesAppView(TemplateView):
    template_name = 'dengue/series.html'


class VectoresAppView(TemplateView):
    template_name = 'dengue/vectores.html'


class VectoresAppView2(TemplateView):
    template_name = 'dengue/vectores2.html'
