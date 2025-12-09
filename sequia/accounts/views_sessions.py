# sequia/accounts/views_sessions.py

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

import requests  # Asegúrate de tener instalado: pip install requests

# Modelos del proyecto Sequía
from sequia.infrastructure import orm_models as models

# Serializer del registro (ya viene de tu API)
from .serializers import RegisterSerializer


# -------------------- REGISTRO DE USUARIO --------------------
def signup_view(request):
    """
    Registro vía formulario HTML usando RegisterSerializer.
    Si es válido, crea el usuario y redirige al login con mensaje de éxito.
    """
    if request.method == "POST":
        data = {
            "username": request.POST.get("username", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "first_name": request.POST.get("first_name", "").strip(),
            "last_name": request.POST.get("last_name", "").strip(),
            "password": request.POST.get("password", ""),
            "password2": request.POST.get("password2", ""),
        }

        ser = RegisterSerializer(data=data)
        if ser.is_valid():
            ser.save()
            messages.success(request, "Cuenta creada exitosamente. Ahora puedes iniciar sesión.")
            return redirect("login")

        # Mostrar errores de validación
        for field, errs in ser.errors.items():
            for err in errs:
                messages.error(request, f"{field}: {err}")

    return render(request, "accounts/register.html")


# -------------------- LOGIN DE USUARIO --------------------
def login_view(request):
    """
    Login clásico por sesión (HTML).
    """
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido, {user.username}")
            return redirect("panel")
        else:
            messages.error(request, "Credenciales incorrectas o usuario inexistente.")

    return render(request, "accounts/login.html")


# -------------------- LOGOUT --------------------
def logout_view(request):
    """
    Cierra la sesión y redirige al login.
    """
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("login")


# -------------------- PANEL PRIVADO --------------------
@login_required
def panel_view(request):
    """
    Panel privado con métricas del proyecto Sequía y clima actual
    consumido desde una API externa (Open-Meteo).
    """

    # 1) Datos del sistema (BD MariaDB)
    medidas_qs = models.Medida.objects.select_related("region", "fuente").all()
    indicadores_qs = models.Indicador.objects.select_related("medida").order_by("-fecha")[:8]

    resumen = {
        "total_medidas": medidas_qs.count(),
        "total_indicadores": models.Indicador.objects.count(),
        "total_fuentes": models.FuenteHidrica.objects.count(),
        "total_regiones": models.Region.objects.count(),
        "promedio_avance": round(
            medidas_qs.aggregate(Avg("avance_pct"))["avance_pct__avg"] or 0, 1
        ),
    }

    # 2) Medidas recientes (para tabla)
    medidas_recientes = medidas_qs.order_by("-fecha_inicio", "-id")[:5]

    # 3) Datos de clima usando API externa (Open-Meteo)
    # Coordenadas por defecto: Santiago, Chile
    lat = request.GET.get("lat", "-33.45")
    lon = request.GET.get("lon", "-70.66")

    clima = None
    clima_error = None

    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
            },
            timeout=5,
        )
        if resp.status_code == 200:
            data = resp.json().get("current_weather", {})
            clima = {
                "lat": lat,
                "lon": lon,
                "temperatura_c": data.get("temperature"),
                "viento_kmh": data.get("windspeed"),
                "direccion_viento": data.get("winddirection"),
                "codigo": data.get("weathercode"),
                "hora": data.get("time"),
            }
        else:
            clima_error = f"Error {resp.status_code} al consultar clima externo."
    except requests.RequestException:
        clima_error = "No se pudo conectar a la API de clima."

    context = {
        "usuario": request.user,
        # KPIs resumen
        "resumen": resumen,
        # Listados
        "medidas": medidas_recientes,
        "indicadores": indicadores_qs,
        # Clima
        "clima": clima,
        "clima_error": clima_error,
        "lat": lat,
        "lon": lon,
    }

    return render(request, "accounts/panel.html", context)
