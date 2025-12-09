# sequia/api/serializers.py
from rest_framework import serializers
from sequia.infrastructure import orm_models as models


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = "__all__"


class FuenteHidricaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FuenteHidrica
        fields = ["id", "tipo", "descripcion", "capacidad_m3d", "energia_renovable"]


class MedidaSerializer(serializers.ModelSerializer):
    # Mostrar anidados (solo lectura)
    region = RegionSerializer(read_only=True)
    fuente = FuenteHidricaSerializer(read_only=True)

    # Escribir por ID (write_only)
    region_id = serializers.PrimaryKeyRelatedField(
        source="region", queryset=models.Region.objects.all(), write_only=True
    )
    fuente_id = serializers.PrimaryKeyRelatedField(
        source="fuente", queryset=models.FuenteHidrica.objects.all(), write_only=True
    )

    class Meta:
        model = models.Medida
        # Campos REALES que nos diste en el shell:
        # ['indicadores','id','nombre','region','fuente','objetivo',
        #  'avance_pct','fecha_inicio','fecha_fin']
        fields = [
            "id", "nombre",
            "region", "region_id",
            "fuente", "fuente_id",
            "objetivo", "avance_pct",
            "fecha_inicio", "fecha_fin",
        ]


class IndicadorSerializer(serializers.ModelSerializer):
    # Mostramos la medida anidada (solo lectura) y permitimos escribir con medida_id
    medida = MedidaSerializer(read_only=True)
    medida_id = serializers.PrimaryKeyRelatedField(
        source="medida", queryset=models.Medida.objects.all(), write_only=True
    )

    class Meta:
        model = models.Indicador
        fields = "__all__"
