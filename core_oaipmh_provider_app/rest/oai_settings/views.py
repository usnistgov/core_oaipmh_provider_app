""" OaiSettings rest api
"""

import requests
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import core_oaipmh_provider_app.components.oai_settings.api as oai_settings_api
from core_main_app.utils.decorators import api_staff_member_required
from core_oaipmh_common_app.commons import exceptions as exceptions_oai
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from core_oaipmh_provider_app.rest import serializers


@api_view(['GET'])
@api_staff_member_required()
def select(request):
    """ Return the OAI-PMH server settings.

    GET http://<server_ip>:<server_port>/<rest_oai_pmh_url>/select/settings

    Returns:
        Response object.

    """
    try:
        settings_ = oai_settings_api.get()
        serializer = serializers.SettingsSerializer(settings_)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@api_staff_member_required()
def check_registry(request):
    """ Check if the registry is available to answer OAI-PMH requests.

    GET http://<server_ip>:<server_port>/<rest_oai_pmh_url>/check/registry

    Returns:
        Response object.

    """
    try:
        base_url = request.build_absolute_uri(reverse("core_oaipmh_provider_app_server_index"))
        http_response = requests.get(base_url)
        is_available = http_response.status_code == status.HTTP_200_OK
        content = OaiPmhMessage.get_message_labelled('Registry available? : {0}.'.format(is_available))

        return Response(content, status=http_response.status_code)
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@api_staff_member_required()
def update(request):
    """ Edit the OAI-PMH server settings.

    PUT http://<server_ip>:<server_port>/<rest_oai_pmh_url>/update/settings

    Params:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"repository_name":"value", "repository_identifier":"value", "enable_harvesting":"True or False"}

    Raises:
        OAIAPISerializeLabelledException: Serialization error.

    """
    try:
        serializer = serializers.UpdateSettingsSerializer(data=request.data)
        if serializer.is_valid():
            settings_ = oai_settings_api.get()
            serializer.update(settings_, serializer.data)
            oai_settings_api.upsert(settings_)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        content = OaiPmhMessage.get_message_labelled('OAI-PMH Settings updated with success.')

        return Response(content, status=status.HTTP_200_OK)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
