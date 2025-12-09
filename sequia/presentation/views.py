# sequia/presentation/views.py
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

# Capa de dominio/aplicación
from sequia.application.services import SequiaService
from sequia.infrastructure.repositories import DjangoSequiaRepository

# Modelos (solo para los CBV y formularios)
from sequia.infrastructure.orm_models import Medida

# Instanciamos el servicio (usa el repo de infraestructura)
service = SequiaService(DjangoSequiaRepository())


class HomeView(TemplateView):
    template_name = "sequia/home.html"


# --------- Medidas (CRUD) ----------
class MedidaList(LoginRequiredMixin, ListView):
    model = Medida
    template_name = "sequia/medida_list.html"
    context_object_name = "items"


class MedidaCreate(LoginRequiredMixin, CreateView):
    model = Medida
    fields = ["nombre", "region", "fuente", "objetivo", "avance_pct", "fecha_inicio", "fecha_fin"]
    template_name = "sequia/medida_form.html"
    success_url = reverse_lazy("medida_list")

    # Usamos el servicio para crear (evita dependencia directa de la vista con el ORM)
    def form_valid(self, form):
        service.crear_medida(**form.cleaned_data)
        return redirect(self.success_url)


class MedidaUpdate(LoginRequiredMixin, UpdateView):
    model = Medida
    fields = ["nombre", "region", "fuente", "objetivo", "avance_pct", "fecha_inicio", "fecha_fin"]
    template_name = "sequia/medida_form.html"
    success_url = reverse_lazy("medida_list")

    # Usamos el servicio para actualizar
    def form_valid(self, form):
        service.actualizar_medida(self.object.pk, **form.cleaned_data)
        return redirect(self.success_url)


class MedidaDelete(LoginRequiredMixin, DeleteView):
    model = Medida
    template_name = "sequia/medida_confirm_delete.html"
    success_url = reverse_lazy("medida_list")

    # Usamos el servicio para eliminar
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        service.eliminar_medida(self.object.pk)
        return redirect(self.success_url)
