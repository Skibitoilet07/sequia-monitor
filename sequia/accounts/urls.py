# sequia/accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Importa las vistas API y las vistas HTML
from .views import RegisterView, MeView, PasswordChangeView
from .views_sessions import login_view, logout_view, panel_view, signup_view

urlpatterns = [
    # --- API REST (JSON Web Tokens) ---
    path("register", RegisterView.as_view(), name="auth_register"),
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("me", MeView.as_view(), name="auth_me"),
    path("password/change", PasswordChangeView.as_view(), name="auth_password_change"),

    # --- Sesiones HTML (Login clásico) ---
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("panel/", panel_view, name="panel"),
    path("signup/", signup_view, name="signup"),  # 👈 Registro desde formulario
]
