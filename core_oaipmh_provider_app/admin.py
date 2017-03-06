"""
Url router for the administration site
"""
from django.contrib import admin
from django.conf.urls import url

from views.admin import views as admin_views
from views.admin import ajax as admin_ajax

admin_urls = [
    url(r'^provider/config', admin_views.identity_view,
        name='core_oaipmh_provider_app_identity'),
    url(r'^provider/registry/check', admin_ajax.check_registry,
        name='core_oaipmh_provider_app_check_registry'),
    url(r'^provider/identity/edit', admin_ajax.edit_identity,
        name='core_oaipmh_provider_app_edit_identity'),
]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
