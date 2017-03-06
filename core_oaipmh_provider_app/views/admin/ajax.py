from django.http.response import HttpResponseBadRequest, HttpResponse
from rest_framework import status
from core_oaipmh_provider_app.views.admin.forms import EditIdentityForm
from core_oaipmh_provider_app.components.oai_settings import api as oai_settings_api
from django.contrib import messages
from django.template import loader
import requests
import json


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
