from django.urls import path

from dengue.views import AnalisisDengueAppView, SeriesAppView, VectoresAppView, VectoresAppView2

app_name = 'dengue'

urlpatterns = [
    path('analisis_dengue', AnalisisDengueAppView.as_view(), name='analisis_dengue'),
    path('series', SeriesAppView.as_view(), name='series'),
    path('vectores', VectoresAppView.as_view(), name='vectores'),
    path('vectores2', VectoresAppView2.as_view(), name='vectores2'),
    ]
