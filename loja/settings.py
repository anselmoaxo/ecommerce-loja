from pathlib import Path
import os
from django.contrib.messages import constants

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-v2_j-9n9kd%_qrfuoz(bh3if27%%z5)(w_gdx60i3$u@ly*+^p"

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "produto",
    "pedido",
    "perfil",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap4",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "loja.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "loja.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "pt-BR"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "templates/static")]


MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


MESSAGE_TAGS = {
    constants.DEBUG: "alert-info",
    constants.ERROR: "alert-danger",
    constants.INFO: "alert-info",
    constants.SUCCESS: "alert-success",
    constants.WARNING: "alert-warning",
}
# Sessão em dias: 60s * 60m * 24h * 1d
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7

# Salvar a cada requisição
SESSION_SAVE_EVERY_REQUEST = False

# Serializer - Padrão JSON
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

# Para sessions em arquivos ao invés da base de dados
# SESSION_ENGINE = "django.contrib.sessions.backends.file"
# SESSION_FILE_PATH = '/home/luizotavio/Desktop/temp'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
