"""Admin AJAX views
"""
import json

import requests
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from django.contrib import messages
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.template import loader
from rest_framework import status

from core_main_app.components.template_version_manager import api as template_version_manager_api
from core_main_app.components.xsl_transformation import api as xsl_transformation_api
from core_oaipmh_provider_app.components.oai_provider_metadata_format import api as oai_provider_metadata_format_api
from core_oaipmh_provider_app.components.oai_provider_set import api as oai_provider_set_api
from core_oaipmh_provider_app.components.oai_provider_set.models import OaiProviderSet
from core_oaipmh_provider_app.components.oai_settings import api as oai_settings_api
from core_oaipmh_provider_app.components.oai_xsl_template import api as  oai_xsl_template_api
from core_oaipmh_provider_app.components.oai_xsl_template.models import OaiXslTemplate
from core_oaipmh_provider_app.views.admin.forms import EditIdentityForm, MetadataFormatForm, EditMetadataFormatForm,\
    TemplateMetadataFormatForm, SetForm, MappingXSLTForm
from core_main_app.commons import exceptions


def check_registry(request):
    """ Check the availability of a registry.
    Args:
        request:

    Returns:

    """
    try:
        http_response = requests.get(request.GET['url'])
        is_available = http_response.status_code == status.HTTP_200_OK
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({'is_available': is_available}), content_type='application/javascript')


def edit_identity(request):
    """ Edit the configuration of the local registry identity.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            form = EditIdentityForm(request.POST)
            if form.is_valid():
                identity = oai_settings_api.get()
                identity.repository_name = request.POST.get('name')
                identity.repository_identifier = request.POST.get('repository_identifier')
                identity.enable_harvesting = request.POST.get('enable_harvesting') == 'on'
                oai_settings_api.upsert(identity)
                messages.add_message(request, messages.SUCCESS, 'Data provider edited with success.')

                return HttpResponse(json.dumps({}), content_type='application/javascript')
            else:
                return HttpResponseBadRequest('Bad entries. Please check your entries')
        elif request.method == 'GET':
            identity = oai_settings_api.get()
            data = {'id': identity.id, 'name': identity.repository_name,
                    'enable_harvesting': identity.enable_harvesting,
                    'repository_identifier': identity.repository_identifier}
            edit_identity_form = EditIdentityForm(data)
            template_name = 'core_oaipmh_provider_app/admin/registry/identity/modals/edit_identity_form.html'
            context = {
                "edit_identity_form": edit_identity_form
            }

            return HttpResponse(json.dumps({'template': loader.render_to_string(template_name, context)}),
                                'application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def add_metadata_format(request):
    """ Add a metadata format.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            form = MetadataFormatForm(request.POST)
            if form.is_valid():
                metadata_prefix = request.POST.get('metadata_prefix')
                schema = request.POST.get('schema')
                req = oai_provider_metadata_format_api.add_metadata_format(metadata_prefix, schema)
                if req.status_code == status.HTTP_201_CREATED:
                    messages.add_message(request, messages.SUCCESS, 'Metadata Format added with success.')

                    return HttpResponse(json.dumps({}), content_type='application/javascript')
                else:
                    data = req.data
                    return HttpResponseBadRequest(data[OaiPmhMessage.label])
            else:
                return HttpResponseBadRequest('Bad entries. Please check your entries')
        elif request.method == 'GET':
            add_metadata_format_form = MetadataFormatForm()
            template_name = 'core_oaipmh_provider_app/admin/registry/metadata_formats/modals/' \
                            'add_metadata_format_form.html'
            context = {
                "add_metadata_format_form": add_metadata_format_form
            }

            return HttpResponse(json.dumps({'template': loader.render_to_string(template_name, context)}),
                                'application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def delete_metadata_format(request):
    """ Delete a metadata format.
    Args:
        request:

    Returns:

    """
    try:
        metadata_format = oai_provider_metadata_format_api.get_by_id(request.GET['id'])
        oai_provider_metadata_format_api.delete(metadata_format)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def edit_metadata_format(request):
    """ Edit the metadata format.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            form = EditMetadataFormatForm(request.POST)
            if form.is_valid():
                metadata_format = oai_provider_metadata_format_api.get_by_id(request.POST['id'])
                metadata_format.metadata_prefix = request.POST.get('metadata_prefix')
                oai_provider_metadata_format_api.upsert(metadata_format)
                messages.add_message(request, messages.SUCCESS, 'Metadata Format edited with success.')

                return HttpResponse(json.dumps({}), content_type='application/javascript')
            else:
                return HttpResponseBadRequest('Bad entries. Please check your entries')
        elif request.method == 'GET':
            metadata_format = oai_provider_metadata_format_api.get_by_id(request.GET['id'])
            data = {'id': metadata_format.id, 'metadata_prefix': metadata_format.metadata_prefix}
            edit_metadata_format_form = EditMetadataFormatForm(data)
            template_name = 'core_oaipmh_provider_app/admin/registry/metadata_formats/modals/' \
                            'edit_metadata_format_form.html'
            context = {
                "edit_metadata_format_form": edit_metadata_format_form
            }

            return HttpResponse(json.dumps({'template': loader.render_to_string(template_name, context)}),
                                'application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def add_template_metadata_format(request):
    """ Add a template metadata format.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            form = TemplateMetadataFormatForm(request.POST)
            if form.is_valid():
                metadata_prefix = request.POST.get('metadata_prefix')
                template = request.POST.get('template')
                req = oai_provider_metadata_format_api.add_template_metadata_format(metadata_prefix, template)
                if req.status_code == status.HTTP_201_CREATED:
                    messages.add_message(request, messages.SUCCESS, 'Metadata Format added with success.')

                    return HttpResponse(json.dumps({}), content_type='application/javascript')
                else:
                    data = req.data
                    return HttpResponseBadRequest(data[OaiPmhMessage.label])
            else:
                return HttpResponseBadRequest('Bad entries. Please check your entries')
        elif request.method == 'GET':
            add_metadata_format_form = TemplateMetadataFormatForm()
            template_name = 'core_oaipmh_provider_app/admin/registry/metadata_formats/modals/' \
                            'add_metadata_format_form.html'
            context = {
                "add_metadata_format_form": add_metadata_format_form
            }

            return HttpResponse(json.dumps({'template': loader.render_to_string(template_name, context)}),
                                'application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def add_set(request):
    """ Add a set.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            form = SetForm(request.POST)
            if form.is_valid():
                set_spec = request.POST.get('set_spec')
                set_name = request.POST.get('set_name')
                templates_manager = request.POST.getlist('templates_manager', [])
                description = request.POST.get('description', '')
                set_ = OaiProviderSet(set_spec=set_spec, set_name=set_name, templates_manager=templates_manager,
                                      description=description)
                oai_provider_set_api.upsert(set_)
                messages.add_message(request, messages.SUCCESS, 'Set added with success.')

                return HttpResponse(json.dumps({}), content_type='application/javascript')
            else:
                return HttpResponseBadRequest('Bad entries. Please check your entries')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def delete_set(request):
    """ Delete a set.
    Args:
        request:

    Returns:

    """
    try:
        set_ = oai_provider_set_api.get_by_id(request.GET['id'])
        oai_provider_metadata_format_api.delete(set_)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def edit_set(request):
    """ Edit a set.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            form = SetForm(request.POST)
            if form.is_valid():
                set_ = oai_provider_set_api.get_by_id(request.POST['id'])
                set_.set_spec = request.POST.get('set_spec')
                set_.set_name = request.POST.get('set_name')
                templates_manager = request.POST.getlist('templates_manager', [])
                set_.templates_manager = [template_version_manager_api.get_by_id(x) for x in templates_manager]
                set_.description = request.POST.get('description', [])
                oai_provider_set_api.upsert(set_)
                messages.add_message(request, messages.SUCCESS, 'Set edited with success.')

                return HttpResponse(json.dumps({}), content_type='application/javascript')
            else:
                return HttpResponseBadRequest('Bad entries. Please check your entries')
        elif request.method == 'GET':
            set_ = oai_provider_set_api.get_by_id(request.GET['id'])
            data = {'id': set_.id, 'set_spec': set_.set_spec, 'set_name': set_.set_name,
                    'description': set_.description, "templates_manager": [x.id for x in set_.templates_manager]}
            edit_set_form = SetForm(data)
            template_name = 'core_oaipmh_provider_app/admin/registry/sets/modals/edit_set_form.html'
            context = {
                "edit_set_form": edit_set_form
            }

            return HttpResponse(json.dumps({'template': loader.render_to_string(template_name, context)}),
                                'application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def add_template_mapping(request):
    """ Add a mapping between a template and a metadata format (thanks to an XSLT).
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            form = MappingXSLTForm(request.POST)
            if form.is_valid():
                metadata_format = request.POST.get('oai_metadata_format')
                template = request.POST.get('template')
                xslt = request.POST.get('xslt')

                oai_xsl_template = OaiXslTemplate(oai_metadata_format=metadata_format, template=template, xslt=xslt)
                oai_xsl_template_api.upsert(oai_xsl_template)
                messages.add_message(request, messages.SUCCESS, 'Mapping added with success.')

                return HttpResponse(json.dumps({}), content_type='application/javascript')
            else:
                return HttpResponseBadRequest('Bad entries. Please check your entries')
    except exceptions.NotUniqueError:
        return HttpResponseBadRequest("This mapping already exists.",
                                      content_type='application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')


def delete_template_mapping(request):
    """ Delete a mapping between a template and a metadata format.
    Args:
        request:

    Returns:

    """
    try:
        oai_xsl_template = oai_xsl_template_api.get_by_id(request.GET['id'])
        oai_xsl_template_api.delete(oai_xsl_template)
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')

    return HttpResponse(json.dumps({}), content_type='application/javascript')


def edit_template_mapping(request):
    """ Edit a mapping between a template and a metadata format.
    Args:
        request:

    Returns:

    """
    try:
        if request.method == 'POST':
            form = MappingXSLTForm(request.POST)
            if form.is_valid():
                oai_xsl_template = oai_xsl_template_api.get_by_id(request.POST['id'])
                xslt = request.POST.get('xslt')
                oai_xsl_template.xslt = xsl_transformation_api.get_by_id(xslt)
                oai_xsl_template_api.upsert(oai_xsl_template)
                messages.add_message(request, messages.SUCCESS, 'Mapping edited with success.')

                return HttpResponse(json.dumps({}), content_type='application/javascript')
            else:
                return HttpResponseBadRequest('Bad entries. Please check your entries')
        elif request.method == 'GET':
            oai_xsl_template = oai_xsl_template_api.get_by_id(request.GET['id'])
            data = {'id': oai_xsl_template.id, 'template': oai_xsl_template.template.id,
                    'oai_metadata_format': oai_xsl_template.oai_metadata_format.id,
                    "xslt": oai_xsl_template.xslt.id}
            edit_mapping_form = MappingXSLTForm(data, edit_mode=True)
            template_name = 'core_oaipmh_provider_app/admin/registry/xsl_template/modals/edit_mapping_form.html'
            context = {
                "edit_mapping_form": edit_mapping_form
            }

            return HttpResponse(json.dumps({'template': loader.render_to_string(template_name, context)}),
                                'application/javascript')
    except Exception, e:
        return HttpResponseBadRequest(e.message, content_type='application/javascript')
