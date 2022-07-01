from rest_framework.relations import StringRelatedField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from dengue.models import Vector


class VectorSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """
    municipio = StringRelatedField()

    class Meta:
        model = Vector
        geo_field = 'geometry'

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = '__all__'
