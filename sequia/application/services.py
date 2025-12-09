from django.core.exceptions import ValidationError
from sequia.domain.contracts import ISequiaRepository

class SequiaService:
    def __init__(self, repo: ISequiaRepository):
        self.repo = repo

    # Medidas
    def crear_medida(self, nombre: str, region, **kwargs):
        if len(nombre.strip()) < 3:
            raise ValidationError("El nombre debe tener al menos 3 caracteres.")
        return self.repo.crear_medida(nombre=nombre, region=region, **kwargs)

    def listar_medidas(self):
        return self.repo.listar_medidas()

    def obtener_medida(self, pk: int):
        return self.repo.obtener_medida(pk)

    def actualizar_medida(self, pk: int, **data):
        if "nombre" in data and len(data["nombre"].strip()) < 3:
            raise ValidationError("Nombre demasiado corto.")
        return self.repo.actualizar_medida(pk, **data)

    def eliminar_medida(self, pk: int):
        self.repo.eliminar_medida(pk)
