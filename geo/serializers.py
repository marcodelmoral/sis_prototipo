from rest_framework import serializers
from rest_framework_gis.fields import GeometryField
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from geo.models import (
    Demograficos, Entidad,
    Localidad,
    Manzana,
    Municipio,
    )


class DemograficosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demograficos
        fields = ["pobtot", "pobmas", "pobfem"]


class DemograficosRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        serializer = DemograficosSerializer(value)
        return serializer.data


class EntidadGeoSerializer(GeoFeatureModelSerializer):
    """A class to serialize locations as GeoJSON compatible data"""
    demograficos = DemograficosRelatedField(many=True, read_only=True)

    class Meta:
        model = Entidad
        geo_field = "geometry"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ("cvegeo", "nomgeo", "cve_ent", "demograficos")


class MunicipioGeoSerializer(GeoFeatureModelSerializer):
    """A class to serialize locations as GeoJSON compatible data"""

    # simplified_geometry = GeometrySerializerMethodField()
    geometry = GeometryField(precision=3, remove_duplicates=True)

    # def get_simplified_geometry(self, obj):
    #     # Returns a new GEOSGeometry, simplified to the specified tolerance
    #     # using the Douglas-Peucker algorithm. A higher tolerance value implies
    #     # fewer points in the output. If no tolerance is provided, it
    #     # defaults to 0.
    #     return obj.geometry.simplify(tolerance=0.01, preserve_topology=True)

    class Meta:
        model = Municipio
        # geo_field = "simplified_geometry"
        geo_field = "geometry"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ("cvegeo", "nomgeo", "cve_ent", "cve_mun")


class MunicipioGeoCountSerializer(GeoFeatureModelSerializer):
    """A class to serialize locations as GeoJSON compatible data"""

    # simplified_geometry = GeometrySerializerMethodField()
    geometry = GeometryField(precision=3, remove_duplicates=True)
    num_casos = serializers.IntegerField()
    vector__fec_sol_aten = serializers.DateField()

    # def get_simplified_geometry(self, obj):
    #     # Returns a new GEOSGeometry, simplified to the specified tolerance
    #     # using the Douglas-Peucker algorithm. A higher tolerance value implies
    #     # fewer points in the output. If no tolerance is provided, it
    #     # defaults to 0.
    #     return obj.geometry.simplify(tolerance=0.01, preserve_topology=True)

    class Meta:
        model = Municipio
        # geo_field = "simplified_geometry"
        geo_field = "geometry"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ("cvegeo", "nomgeo", 'num_casos', 'vector__fec_sol_aten')


class LocalidadGeoSerializer(GeoFeatureModelSerializer):
    """A class to serialize locations as GeoJSON compatible data"""
    ambito = serializers.CharField(source='get_ambito_display')

    class Meta:
        model = Localidad
        geo_field = "geometry"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = ("cvegeo", "nomgeo", "cve_ent", "cve_mun", "cve_loc", "ambito")


class ManzanaGeoSerializer(GeoFeatureModelSerializer):
    """A class to serialize locations as GeoJSON compatible data"""
    ambito = serializers.CharField(source='get_ambito_display')
    tipo = serializers.CharField(source='get_tipo_display')

    class Meta:
        model = Manzana
        geo_field = "geometry"

        # you can also explicitly declare which fields you want to include
        # as with a ModelSerializer.
        fields = (
            "cvegeo",
            "cve_ent",
            "cve_mun",
            "cve_loc",
            "cve_ageb",
            "cve_mza",
            "ambito",
            "tipo"
            )
