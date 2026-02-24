from pathlib import Path
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "/static/"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"  # opcional
USE_I18N = True
USE_TZ = True

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dev-secret-key'
DEBUG = False
ALLOWED_HOSTS = ["hellerfinance.com", "www.hellerfinance.com", "S72.62.211.122"]


INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "website",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = "gedeonfigueiredo@gmail.com"
EMAIL_HOST_PASSWORD = "t b r h y u d k p a s z j a t o"

DEFAULT_FROM_EMAIL = "Heller Finance <gedeonfigueiredo@gmail.com>"
SERVER_EMAIL = "gedeonfigueiredo@gmail.com"

# opcional
SEND_CONFIRMATION_TO_CLIENT = True

JAZZMIN_SETTINGS = {
    "site_title": "Heller Finance Admin",
    "site_header": "Heller Finance",
    "site_brand": "Life Insurance System",
    "welcome_sign": "Bem-vindo ao painel administrativo",
    "search_model": ["website.TermRate"],
    "topmenu_links": [
        {"name": "Site", "url": "/", "new_window": True},
    ],
    "icons": {
        "website.TermRate": "fas fa-file-invoice-dollar",
    },
    "show_sidebar": True,
    "navigation_expanded": True,
    "theme": "darkly",  # 🔥 bonito demais
    
     "topmenu_links": [
        {"name": "Sair", "url": "admin:logout", "new_window": False},
    ],
}

LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/admin/"
LOGOUT_REDIRECT_URL = "/admin/login/"


