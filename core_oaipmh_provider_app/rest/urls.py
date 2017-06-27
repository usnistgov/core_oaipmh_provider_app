"""Url router for the REST API
"""
from django.conf.urls import url
from core_oaipmh_provider_app.rest.oai_settings import views as oai_settings_views
from core_oaipmh_provider_app.rest.oai_provider_metadata_format import views as oai_metadata_format_views
from core_oaipmh_provider_app.rest.oai_provider_set import views as oai_set_views


urlpatterns = [
    url(r'^select/settings$', oai_settings_views.select,
        name='core_oaipmh_provider_app_rest_select_settings'),
    url(r'^check/registry$', oai_settings_views.check_registry,
        name='core_oaipmh_provider_app_rest_check_registry'),
    url(r'^update/settings$', oai_settings_views.update,
        name='core_oaipmh_provider_app_rest_update_settings'),
    url(r'^select/metadata_format$', oai_metadata_format_views.select_metadata_format,
        name='core_oaipmh_provider_app_rest_select_metadata_format'),
    url(r'^select/all/metadata_formats', oai_metadata_format_views.select_all_metadata_formats,
        name='core_oaipmh_provider_app_rest_select_all_metadata_formats'),
    url(r'^add/metadata_format$', oai_metadata_format_views.add_metadata_format,
        name='core_oaipmh_provider_app_rest_add_metadata_format'),
    url(r'^add/template_metadata_format$', oai_metadata_format_views.add_template_metadata_format,
        name='core_oaipmh_provider_app_rest_add_template_metadata_format'),
    url(r'^delete/metadata_format$', oai_metadata_format_views.delete_metadata_format,
        name='core_oaipmh_provider_app_rest_update_delete_metadata_format'),
    url(r'^update/metadata_format$', oai_metadata_format_views.update_metadata_format,
        name='core_oaipmh_provider_app_rest_update_update_metadata_format'),
    url(r'^select/set$', oai_set_views.select_set,
        name='core_oaipmh_provider_app_rest_select_set'),
    url(r'^select/all/sets', oai_set_views.select_all_sets,
        name='core_oaipmh_provider_app_rest_select_all_sets'),
    url(r'^add/set$', oai_set_views.add_set,
        name='core_oaipmh_provider_app_rest_add_set'),
    url(r'^update/set$', oai_set_views.update_set,
        name='core_oaipmh_provider_app_rest_update_set'),
    url(r'^delete/set', oai_set_views.delete_set,
        name='core_oaipmh_provider_app_rest_delete_set'),
    url(r'^mapping/template/metadata_format/xslt', oai_metadata_format_views.template_to_metadata_format_mapping_xslt,
        name='core_oaipmh_provider_app_rest_mapping_template_mf_xslt'),
    url(r'^unmapping/template/metadata_format/xslt',
        oai_metadata_format_views.template_to_metadata_format_unmapping_xslt,
        name='core_oaipmh_provider_app_rest_unmapping_template_mf_xslt'),
]
