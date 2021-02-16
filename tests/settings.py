import os

os.environ["PYTHONBREAKPOINT"] = "ipdb.set_trace"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True

ROOT_URLCONF = "example.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
            ]
        },
    }
]

SECRET_KEY = "NOTREALLY"
PAYMENT_HOST = "example.com"

INSTALLED_APPS = ["django.contrib.sites", "core_helpers"]

WSGI_APPLICATION = "example.wsgi.application"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}


TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True
