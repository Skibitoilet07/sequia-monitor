from django.urls import path
from .views import HomeView, MedidaList, MedidaCreate, MedidaUpdate, MedidaDelete

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("medidas/", MedidaList.as_view(), name="medida_list"),
    path("medidas/nueva/", MedidaCreate.as_view(), name="medida_create"),
    path("medidas/<int:pk>/editar/", MedidaUpdate.as_view(), name="medida_update"),
    path("medidas/<int:pk>/eliminar/", MedidaDelete.as_view(), name="medida_delete"),
]
