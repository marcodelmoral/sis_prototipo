from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from sis_prototipo.apps.vectores.models import Vector


class VectorGeoSerializer(GeoFeatureModelSerializer):
    """A class to serialize locations as GeoJSON compatible data"""

    municipio = StringRelatedField()

    class Meta:
        model = Vector
        geo_field = "geometry"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = "__all__"


class VectorSerializer(ModelSerializer):
    class Meta:
        model = Vector
        fields = "__all__"
