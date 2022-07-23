from rest_framework import routers

from dengue import api_views as dengue_views

router = routers.DefaultRouter()
vectores = router.register('vectores', dengue_views.VectorViewSet)
