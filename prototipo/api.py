from rest_framework import routers

from dengue import api_views as dengue_views
from geo import api_views as geo_views

router = routers.DefaultRouter()
vectores = router.register("vectores", dengue_views.VectorViewSet)
entidades = router.register("entidades", geo_views.EntidadGeoViewSet)
municipio = router.register("municipios", geo_views.MunicipioGeoViewSet)
localidades = router.register("localidades", geo_views.LocalidadGeoViewSet)
manzanas = router.register("manzanas", geo_views.ManzanaGeoViewSet)
