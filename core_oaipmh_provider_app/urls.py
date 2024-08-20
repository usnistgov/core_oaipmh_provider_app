""" Url router for OAI-PMH provider application
"""

from django.conf.urls import include
from django.urls import re_path

from core_oaipmh_provider_app.views.user.views import OAIProviderView, get_xsd

urlpatterns = [
    re_path(r"^rest/", include("core_oaipmh_provider_app.rest.urls")),
    re_path(
        r"^XSD/(?P<title>.*)/(?:(?P<version_number>\d+)/)$",
        get_xsd,
        name="core_oaipmh_provider_app_get_xsd",
    ),
    re_path(
        r"^$",
        OAIProviderView.as_view(),
        name="core_oaipmh_provider_app_server_index",
    ),
]
