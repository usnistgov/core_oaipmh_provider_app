"""
Url router for the administration site
"""
from django.conf.urls import url
from django.contrib import admin
from views.admin import ajax as admin_ajax
from views.admin import views as admin_views

admin_urls = [
    url(r'^provider/identity/config', admin_views.identity_view,
        name='core_oaipmh_provider_app_identity'),
    url(r'^provider/registry/check', admin_ajax.check_registry,
        name='core_oaipmh_provider_app_check_registry'),
    url(r'^provider/identity/edit', admin_ajax.edit_identity,
        name='core_oaipmh_provider_app_edit_identity'),
    url(r'^provider/metadata_formats/config', admin_views.metadata_formats_view,
        name='core_oaipmh_provider_app_metadata_formats'),
    url(r'^provider/metadata_formats/add', admin_ajax.add_metadata_format,
        name='core_oaipmh_provider_app_add_metadata_format'),
    url(r'^provider/metadata_formats/delete', admin_ajax.delete_metadata_format,
        name='core_oaipmh_provider_app_delete_metadata_format'),
    url(r'^provider/metadata_formats/edit', admin_ajax.edit_metadata_format,
        name='core_oaipmh_provider_app_edit_metadata_format'),
    url(r'^provider/metadata_formats/template/add', admin_ajax.add_template_metadata_format,
        name='core_oaipmh_provider_app_add_template_metadata_format'),
    url(r'^provider/sets/config', admin_views.sets_view, name='core_oaipmh_provider_app_sets'),
    url(r'^provider/sets/add', admin_ajax.add_set, name='core_oaipmh_provider_app_add_set'),
    url(r'^provider/sets/delete', admin_ajax.delete_set, name='core_oaipmh_provider_app_delete_set'),
    url(r'^provider/sets/edit', admin_ajax.edit_set, name='core_oaipmh_provider_app_edit_set'),

    url(r'^provider/xslt_template/mapping/(?P<metadata_format_id>\w+)', admin_views.xsl_template_view,
        name='core_oaipmh_provider_app_xslt_template_mapping'),
    url(r'^provider/xslt_template/add', admin_ajax.add_template_mapping,
        name='core_oaipmh_provider_app_add_template_mapping'),
    url(r'^provider/xslt_template/delete', admin_ajax.delete_template_mapping,
        name='core_oaipmh_provider_app_delete_template_mapping'),
    url(r'^provider/xslt_template/edit', admin_ajax.edit_template_mapping,
        name='core_oaipmh_provider_app_edit_template_mapping'),




]

urls = admin.site.get_urls()
admin.site.get_urls = lambda: admin_urls + urls
