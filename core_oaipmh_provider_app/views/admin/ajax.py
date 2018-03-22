"""Admin AJAX views
"""
import json

import requests
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.template import loader
from rest_framework import status

from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import NotUniqueError
from core_main_app.views.common.ajax import EditObjectModalView
from core_oaipmh_provider_app.components.oai_provider_metadata_format import api as \
    oai_provider_metadata_format_api
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import \
    OaiProviderMetadataFormat
from core_oaipmh_provider_app.components.oai_provider_set import api as oai_provider_set_api
from core_oaipmh_provider_app.components.oai_provider_set.models import OaiProviderSet
from core_oaipmh_provider_app.components.oai_settings import api as oai_settings_api
from core_oaipmh_provider_app.components.oai_settings.models import OaiSettings
from core_oaipmh_provider_app.components.oai_xsl_template import api as  oai_xsl_template_api
from core_oaipmh_provider_app.components.oai_xsl_template.models import OaiXslTemplate
from core_oaipmh_provider_app.views.admin.forms import EditIdentityForm, MetadataFormatForm, \
    EditMetadataFormatForm, TemplateMetadataFormatForm, SetForm, MappingXSLTForm


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


class EditIdentityView(EditObjectModalView):
    form_class = EditIdentityForm
    model = OaiSettings
    success_url = reverse_lazy("admin:core_oaipmh_provider_app_identity")
    success_message = 'Data provider edited with success.'

    def _save(self, form):
        # Save treatment.
        try:
            oai_settings_api.upsert(self.object)
        except Exception, e:
            form.add_error(None, e.message)


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


class EditMetadataFormatView(EditObjectModalView):
    form_class = EditMetadataFormatForm
    model = OaiProviderMetadataFormat
    success_url = reverse_lazy("admin:core_oaipmh_provider_app_metadata_formats")
    success_message = 'Metadata Format edited with success.'

    def _save(self, form):
        # Save treatment.
        try:
            oai_provider_metadata_format_api.upsert(self.object)
        except NotUniqueError:
            form.add_error(None, "A Metadata Format with the same prefix already exists. Please "
                                 "choose another prefix.")
        except Exception, e:
            form.add_error(None, e.message)


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


class EditSetView(EditObjectModalView):
    form_class = SetForm
    model = OaiProviderSet
    success_url = reverse_lazy("admin:core_oaipmh_provider_app_sets")
    success_message = 'Set edited with success.'

    def _save(self, form):
        # Save treatment.
        try:
            oai_provider_set_api.upsert(self.object)
        except Exception, e:
            form.add_error(None, e.message)

    def get_initial(self):
        initial = super(EditSetView, self).get_initial()
        initial['templates_manager'] = [x.id for x in self.object.templates_manager]

        return initial


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


class EditTemplateMappingView(EditObjectModalView):
    form_class = MappingXSLTForm
    model = OaiXslTemplate
    success_message = 'Mapping edited with success.'

    def _save(self, form):
        # Save treatment.
        try:
            oai_xsl_template_api.upsert(self.object)
        except Exception, e:
            form.add_error(None, e.message)

    def get_initial(self):
        initial = super(EditTemplateMappingView, self).get_initial()
        initial['xslt'] = self.object.xslt.id
        initial['template'] = self.object.template.id

        return initial

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
            arguments."""
        # grab the current set of form #kwargs
        kwargs = super(EditTemplateMappingView, self).get_form_kwargs()
        # Update the kwargs
        kwargs['edit_mode'] = True

        return kwargs

    def get_success_url(self):
        return reverse_lazy("admin:core_oaipmh_provider_app_xslt_template_mapping",
                            args=(self.object.oai_metadata_format.id,))
