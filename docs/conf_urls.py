from django.conf.urls import url, include
from django.contrib import admin

from core_oaipmh_provider_app import urls as core_oaipmh_provider_app_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
] + core_oaipmh_provider_app_urls.urlpatterns
