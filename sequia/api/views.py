# sequia/api/views.py
import os
print("OPENWEATHER:", os.getenv("OPENWEATHER_API_KEY"))
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from sequia.infrastructure import orm_models as models
from rest_framework.filters import SearchFilter, OrderingFilter
from .serializers import FuenteHidricaSerializer
from .serializers import (
    RegionSerializer,
    FuenteHidricaSerializer,
    MedidaSerializer,
    IndicadorSerializer,
)


class IsAuthenticatedOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    """Lectura pública; escritura autenticada."""
    pass


class RegionViewSet(viewsets.ModelViewSet):
    queryset = models.Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre"]
    ordering = ["nombre"]


class FuenteHidricaViewSet(viewsets.ModelViewSet):
    queryset = models.FuenteHidrica.objects.all().order_by("id")
    serializer_class = FuenteHidricaSerializer
    permission_classes = [permissions.AllowAny]   # o tu permiso real

    # OJO: aquí estaban usando 'nombre' — cámbialo a 'tipo' y/o 'descripcion'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Busca por tipo o descripción
    search_fields = ["tipo", "descripcion"]

    # Permite ordenar por estos campos en ?ordering=
    ordering_fields = ["id", "tipo", "capacidad_m3d", "energia_renovable"]

    # Filtros exactos en querystring (?tipo=Embalse&energia_renovable=true ...)
    filterset_fields = {
        "tipo": ["exact", "icontains"],
        "descripcion": ["icontains"],
        "capacidad_m3d": ["exact", "gte", "lte"],
        "energia_renovable": ["exact"],  # boolean
    }

class MedidaViewSet(viewsets.ModelViewSet):
    # Campos REALES: region, fuente, nombre, objetivo, avance_pct, fecha_inicio, fecha_fin
    queryset = models.Medida.objects.select_related("region", "fuente")
    serializer_class = MedidaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtros seguros (existen en tu modelo)
    filterset_fields = ["region", "fuente"]

    # Búsqueda por texto
    search_fields = ["nombre", "objetivo"]

    # Orden recomendado por fecha_inicio
    ordering = ["-fecha_inicio"]


class IndicadorViewSet(viewsets.ModelViewSet):
    queryset = models.Indicador.objects.select_related("medida", "medida__region", "medida__fuente")
    serializer_class = IndicadorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filtros seguros aunque no conozcamos todos los campos de Indicador
    filterset_fields = ["medida"]

    # Búsqueda por nombre de la medida relacionada
    search_fields = ["medida__nombre"]

    # Orden simple y seguro
    ordering = ["-id"]

class ClimaOneCallView(APIView):
    """
    Endpoint que consume una API externa de clima (Open-Meteo, sin API key).
    Uso:
        /api/clima/?lat=-33.45&lon=-70.66
    """

    permission_classes = []  # Solo lectura, público

    def get(self, request, *args, **kwargs):
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")

        if not lat or not lon:
            return Response(
                {"error": "Debes enviar lat y lon, ejemplo: /api/clima/?lat=-33.45&lon=-70.66"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": "true",
        }

        try:
            resp = requests.get(url, params=params, timeout=5)
        except requests.RequestException:
            return Response(
                {"error": "No se pudo conectar a la API externa (Open-Meteo)."},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        if resp.status_code != 200:
            return Response(
                {
                    "error": "Respuesta inválida de la API externa",
                    "status": resp.status_code,
                    "body": resp.text,
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        data = resp.json()
        current = data.get("current_weather", {})

        resultado = {
            "lat": lat,
            "lon": lon,
            "temperatura_c": current.get("temperature"),
            "viento_kmh": current.get("windspeed"),
            "direccion_viento_grados": current.get("winddirection"),
            "codigo_clima": current.get("weathercode"),
            "hora_medicion": current.get("time"),
        }

        return Response(resultado, status=status.HTTP_200_OK)