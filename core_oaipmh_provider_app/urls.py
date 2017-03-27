""" Url router for OAI-PMH provider application
"""
from django.conf.urls import url
from core_oaipmh_provider_app.views.user.views import OAIProviderView
from core_oaipmh_provider_app.views.user.views import get_xsd
urlpatterns = [
    # Put the schema name in the schema attribute (/XSD/schemaNameInTheURL)
    url(r'^(?i)XSD/(?P<title>.*)/(?:(?P<version_number>\d+)/)', get_xsd, name="core_oaipmh_harvester_app_get_xsd"),
    url(r'^', OAIProviderView.as_view()),
]
