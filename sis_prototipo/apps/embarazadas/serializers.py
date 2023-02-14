from rest_framework_gis.serializers import GeoFeatureModelSerializer
from django.core.serializers.base import Serializer as BaseSerializer
from django.core.serializers.python import Serializer as PythonSerializer
from django.contrib.gis.serializers.geojson import Serializer as JsonSerializer

from sis_prototipo.apps.embarazadas.models import Embarazada


class ExtBaseSerializer(BaseSerializer):

    def serialize_property(self, obj):
        model = type(obj)
        for field in self.selected_fields:
            if hasattr(model, field) and type(getattr(model, field)) == property:
                    self.handle_prop(obj, field)

    def handle_prop(self, obj, field):
        self._current[field] = getattr(obj, field)

    def end_object(self, obj):
        self.serialize_property(obj)

        super(ExtBaseSerializer, self).end_object(obj)


class ExtPythonSerializer(ExtBaseSerializer, PythonSerializer):
    pass


class ExtJsonSerializer(ExtPythonSerializer, JsonSerializer):
    pass


class EmbarazadaSerializer(GeoFeatureModelSerializer):
    """ A class to serialize locations as GeoJSON compatible data """

    class Meta:
        model = Embarazada
        geo_field = "LOC"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ('contenido', 'NSS')

