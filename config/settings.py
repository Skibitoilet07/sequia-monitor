"""
Configuración de Django para el proyecto Sequia.
Incluye API REST (DRF + JWT), MariaDB, CORS y zona horaria de Chile.
"""

from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

# -----------------------------------------------------------
# RUTAS BASE
# -----------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables desde .env (si existe)
load_dotenv()

# -----------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------------------------------
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-1fxqzdnk=93lc6zbf(&f^3&oe93^do!uow3x1z8zz5f4cz5!#f"
)
DEBUG = True
ALLOWED_HOSTS = [
    'sequia-monitor.onrender.com',
    'localhost',
    '127.0.0.1',
]

# -----------------------------------------------------------
# APLICACIONES INSTALADAS
# -----------------------------------------------------------
INSTALLED_APPS = [
    # Django por defecto
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Aplicaciones del proyecto
    "sequia.apps.SequiaConfig",
    "sequia.accounts",  # 👈 app creada para registro/login

    # Librerías externas
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
]

# -----------------------------------------------------------
# MIDDLEWARE
# -----------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # 👈 siempre primero
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------------------------------------
# CONFIGURACIÓN DE URLS Y TEMPLATES
# -----------------------------------------------------------
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Carpeta global de templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# -----------------------------------------------------------
# BASE DE DATOS (MariaDB / MySQL)
# -----------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # MariaDB usa el backend MySQL
        "NAME": os.getenv("DB_NAME", "sequia_db"),
        "USER": os.getenv("DB_USER", "sequia_user"),
        "PASSWORD": os.getenv("DB_PASS", "Tu_Clave_Segura_2025"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}

# -----------------------------------------------------------
# CONFIGURACIÓN REST FRAMEWORK
# -----------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
}

# -----------------------------------------------------------
# CONFIGURACIÓN SIMPLE_JWT (autenticación por tokens)
# -----------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
}

# -----------------------------------------------------------
# CORS (Cross-Origin Resource Sharing)
# -----------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True  # 👈 solo para desarrollo
# En producción, cambia a:
# CORS_ALLOW_ALL_ORIGINS = False
# CORS_ALLOWED_ORIGINS = ["https://tu-frontend.com", "http://localhost:5173"]

# -----------------------------------------------------------
# VALIDADORES DE CONTRASEÑAS
# -----------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------------
# INTERNACIONALIZACIÓN
# -----------------------------------------------------------
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------------
# ARCHIVOS ESTÁTICOS
# -----------------------------------------------------------
STATIC_URL = "static/"

# -----------------------------------------------------------
# CONFIGURACIÓN LOGIN / LOGOUT (admin o sesiones)
# -----------------------------------------------------------
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "panel"
LOGOUT_REDIRECT_URL = "home"

# -----------------------------------------------------------
# CONFIGURACIÓN DEFAULTS
# -----------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Seguridad y Sesiones ---
SESSION_COOKIE_AGE = 1800          # 30 minutos
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
CSRF_COOKIE_SECURE = False         # True en producción (HTTPS)
SESSION_COOKIE_SECURE = False      # True en producción
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

