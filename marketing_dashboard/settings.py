from pathlib import Path
from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY")

DEBUG = env.bool("IS_DEVELOPMENT", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", [])
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", [])
CSRF_COOKIE_SECURE = not DEBUG

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "django_filters",
    "commons",
    "campaigns",
    "campaign_metrics",
    "keywords",
    "keyword_metrics",
    "regions",
    "ads",
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

ROOT_URLCONF = "marketing_dashboard.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "marketing_dashboard.wsgi.application"


STATIC_URL = "/static/"
STATIC_ROOT = env("STATIC_ROOT")

MEDIA_URL = "/media/"
MEDIA_ROOT = env("MEDIA_ROOT")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
}

import logging

logging.basicConfig(level="WARNING")

SCRAPY = {
    "ROBOTSTXT_OBEY": False,
    "USER_AGENT": "Mozilla/5.0 (Windows; Windows NT 10.4; WOW64; en-US) AppleWebKit/536.48 (KHTML, like Gecko) Chrome/50.0.3290.332 Safari/537.7 Edge/17.35740",
    "CONCURRENT_REQUESTS": 8,
    "METAREFRESH_ENABLED": False,
    "DOWNLOAD_TIMEOUT": 20,
    "RETRY_ENABLED": False,
    "COOKIES_ENABLED": False,
    "HTTPCACHE_ENABLED": True,
    "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
    "SPIDER_MIDDLEWARES": {
        "scrapy_sticky_meta_params.middleware.StickyMetaParamsMiddleware": 550,
    },
    "DEPTH_LIMIT": 1,
    "DEPTH_PRIORITY": 1,
    "DOWNLOAD_DELAY": 1,
    "EXTENSIONS": {
        "scrapy.extensions.closespider.CloseSpider": 500,
    },
}
