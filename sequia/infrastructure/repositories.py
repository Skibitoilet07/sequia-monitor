from typing import Dict, Any, Iterable
from django.forms.models import model_to_dict
from .orm_models import Region, Medida

def _dto(obj):
    d = model_to_dict(obj)
    d["id"] = obj.id
    return d

class DjangoSequiaRepository:
    # Regiones
    def regiones(self) -> Iterable[Dict[str, Any]]:
        return [_dto(r) for r in Region.objects.all().order_by("nombre")]

    # Medidas
    def crear_medida(self, **data) -> Dict[str, Any]:
        return _dto(Medida.objects.create(**data))

    def listar_medidas(self) -> Iterable[Dict[str, Any]]:
        return [_dto(m) for m in Medida.objects.select_related("region", "fuente").all()]

    def obtener_medida(self, pk: int) -> Dict[str, Any]:
        return _dto(Medida.objects.get(pk=pk))

    def actualizar_medida(self, pk: int, **data) -> Dict[str, Any]:
        obj = Medida.objects.get(pk=pk)
        for k, v in data.items():
            setattr(obj, k, v)
        obj.save()
        return _dto(obj)

    def eliminar_medida(self, pk: int) -> None:
        Medida.objects.filter(pk=pk).delete()
