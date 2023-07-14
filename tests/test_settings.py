""" Test settings
"""

import os
from os.path import dirname, realpath, join


SECRET_KEY = "fake-key"

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    # Extra apps
    "django_celery_beat",
    # Local apps
    "tests",
    "core_main_app",
    "core_oaipmh_common_app",
    "core_oaipmh_provider_app",
]

OAI_PROVIDER_ROOT = dirname(realpath(__file__))
OAI_ADMINS = ["admin@example.com"]

ALLOWED_HOSTS = ["testserver"]

# IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            join(
                dirname(dirname(os.path.realpath(__file__))),
                "core_oaipmh_provider_app",
                "templates",
            )
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

ROOT_URLCONF = "core_oaipmh_provider_app.urls"

CAN_SET_PUBLIC_DATA_TO_PRIVATE = False
CAN_SET_WORKSPACE_PUBLIC = False
CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

MONGODB_INDEXING = False
MONGODB_ASYNC_SAVE = False
ENABLE_SAML2_SSO_AUTH = False
BOOTSTRAP_VERSION = "5.1.3"
