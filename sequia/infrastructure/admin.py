from django.contrib import admin
from .orm_models import Region, FuenteHidrica, Medida, Indicador

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ["nombre"]

@admin.register(FuenteHidrica)
class FuenteAdmin(admin.ModelAdmin):
    list_display = ("tipo", "capacidad_m3d", "energia_renovable")
    list_filter = ("tipo", "energia_renovable")

@admin.register(Medida)
class MedidaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "region", "fuente", "avance_pct", "fecha_inicio", "fecha_fin")
    list_filter = ("region", "fuente")
    search_fields = ("nombre",)

@admin.register(Indicador)
class IndicadorAdmin(admin.ModelAdmin):
    list_display = ("medida", "fecha", "volumen_reutilizado_m3d", "perdidas_pct", "nivel_freatico_m", "caudal_ecologico_pct")
    list_filter = ("fecha", "medida")
