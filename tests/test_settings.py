import os
from os.path import dirname, realpath, join

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    "tests",
]
OAI_PROVIDER_ROOT = dirname(realpath(__file__))
ALLOWED_HOSTS=['testserver']
TEMPLATES=[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            join(dirname(dirname(os.path.realpath(__file__))), 'core_oaipmh_provider_app',
                                                               'templates')
        ],
    },
]
