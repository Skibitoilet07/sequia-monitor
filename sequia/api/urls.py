# sequia/api/urls.py
from .views import ClimaOneCallView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegionViewSet,
    FuenteHidricaViewSet,
    MedidaViewSet,
    IndicadorViewSet,
)

router = DefaultRouter()
router.register(r"regiones", RegionViewSet)
router.register(r"fuentes", FuenteHidricaViewSet)
router.register(r"medidas", MedidaViewSet)
router.register(r"indicadores", IndicadorViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("clima/", ClimaOneCallView.as_view(), name="clima-api"),

]
