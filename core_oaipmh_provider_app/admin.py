"""
Url router for the administration site
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_main_app.admin import core_admin_site
from core_oaipmh_provider_app.components.oai_data.models import OaiData
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import (
    OaiProviderMetadataFormat,
)
from core_oaipmh_provider_app.components.oai_provider_set.models import OaiProviderSet
from core_oaipmh_provider_app.components.oai_request_page.models import OaiRequestPage
from core_oaipmh_provider_app.components.oai_settings.models import OaiSettings
from core_oaipmh_provider_app.components.oai_xsl_template.models import OaiXslTemplate
from core_oaipmh_provider_app.views.admin import (
    ajax as admin_ajax,
    views as admin_views,
)

admin.site.register(OaiData)
admin.site.register(OaiProviderMetadataFormat)
admin.site.register(OaiProviderSet)
admin.site.register(OaiRequestPage)
admin.site.register(OaiSettings)
admin.site.register(OaiXslTemplate)

admin_urls = [
    re_path(
        r"^provider/identity/config",
        admin_views.identity_view,
        name="core_oaipmh_provider_app_identity",
    ),
    re_path(
        r"^provider/registry/check",
        admin_ajax.check_registry,
        name="core_oaipmh_provider_app_check_registry",
    ),
    re_path(
        r"^provider/identity/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditIdentityView.as_view()),
        name="core_oaipmh_provider_app_edit_identity",
    ),
    re_path(
        r"^provider/metadata_formats/config",
        admin_views.metadata_formats_view,
        name="core_oaipmh_provider_app_metadata_formats",
    ),
    re_path(
        r"^provider/metadata_formats/add",
        staff_member_required(admin_ajax.AddMetadataFormatView.as_view()),
        name="core_oaipmh_provider_app_add_metadata_format",
    ),
    re_path(
        r"^provider/metadata_formats/(?P<pk>[\w-]+)/delete/$",
        staff_member_required(admin_ajax.DeleteMetadataFormatView.as_view()),
        name="core_oaipmh_provider_app_delete_metadata_format",
    ),
    re_path(
        r"^provider/metadata_formats/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditMetadataFormatView.as_view()),
        name="core_oaipmh_provider_app_edit_metadata_format",
    ),
    re_path(
        r"^provider/metadata_formats/template/add",
        staff_member_required(admin_ajax.AddTemplateMetadataFormatView.as_view()),
        name="core_oaipmh_provider_app_add_template_metadata_format",
    ),
    re_path(
        r"^provider/sets/config",
        admin_views.sets_view,
        name="core_oaipmh_provider_app_sets",
    ),
    re_path(
        r"^provider/sets/add",
        staff_member_required(admin_ajax.AddSetView.as_view()),
        name="core_oaipmh_provider_app_add_set",
    ),
    re_path(
        r"^provider/sets/(?P<pk>[\w-]+)/delete/$",
        staff_member_required(admin_ajax.DeleteSetView.as_view()),
        name="core_oaipmh_provider_app_delete_set",
    ),
    re_path(
        r"^provider/sets/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditSetView.as_view()),
        name="core_oaipmh_provider_app_edit_set",
    ),
    re_path(
        r"^provider/xslt_template/mapping/(?P<metadata_format_id>\w+)",
        admin_views.xsl_template_view,
        name="core_oaipmh_provider_app_xslt_template_mapping",
    ),
    re_path(
        r"^provider/xslt_template/(?P<oai_metadata_format>[\w-]+)/add/$",
        staff_member_required(admin_ajax.AddTemplateMappingView.as_view()),
        name="core_oaipmh_provider_app_add_template_mapping",
    ),
    re_path(
        r"^provider/xslt_template/(?P<pk>[\w-]+)/delete/$",
        staff_member_required(admin_ajax.DeleteTemplateMappingView.as_view()),
        name="core_oaipmh_provider_app_delete_template_mapping",
    ),
    re_path(
        r"^provider/xslt_template/(?P<pk>[\w-]+)/edit/$",
        staff_member_required(admin_ajax.EditTemplateMappingView.as_view()),
        name="core_oaipmh_provider_app_edit_template_mapping",
    ),
]

urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
