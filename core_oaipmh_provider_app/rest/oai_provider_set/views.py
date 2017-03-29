""" OaiProviderSet rest api
"""

from core_main_app.commons import exceptions
from core_main_app.utils.decorators import api_staff_member_required
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import core_oaipmh_provider_app.components.oai_provider_set.api as oai_provider_set_api
from core_oaipmh_common_app.commons import exceptions as exceptions_oai
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from core_oaipmh_provider_app.rest import serializers


@api_view(['GET'])
@api_staff_member_required()
def select_set(request):
    """ Get a set by its id.

    GET http://<server_ip>:<server_port>/<rest_oai_pmh_url>/select/set

    Params:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"set_id":"value"}

    Raises:
        OAIAPISerializeLabelledException: Serialization error.

    """
    try:
        serializer = serializers.SetIdSerializer(data=request.query_params)
        if serializer.is_valid():
            set_ = oai_provider_set_api.get_by_id(serializer.data.get('set_id'))
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.OaiProviderSetSerializer(set_)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No Set found with the given id.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@api_staff_member_required()
def select_all_sets(request):
    """ Return all sets.

    GET http://<server_ip>:<server_port>/<rest_oai_pmh_url>/select/all/sets

    Returns:
        Response object.

    """
    try:
        sets = oai_provider_set_api.get_all()
        serializer = serializers.OaiProviderSetSerializer(sets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def add_set(request):
    """ Add a new set.

    POST http://<server_ip>:<server_port>/<rest_oai_pmh_url>/add/set

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"set_spec":"value", "set_name":"value", "templates_manager": ["id1", "id2"], "description":"value"}

    Raises:
        OAIAPISerializeLabelledException: Serialization error.

    """
    try:
        serializer = serializers.AddSetSerializer(data=request.data)
        if serializer.is_valid():
            set_ = serializer.create(serializer.data)
            oai_provider_set_api.upsert(set_)
            content = OaiPmhMessage.get_message_labelled('Set added with success.')

            return Response(content, status=status.HTTP_201_CREATED)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def update_set(request):
    """ Update set.

    POST http://<server_ip>:<server_port>/<rest_oai_pmh_url>/update/set

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"set_id":"value", "set_spec":"value", "set_name":"value", "templates_manager": ["id1", "id2"], "description":"value"}

    Raises:
        OAIAPISerializeLabelledException: Serialization error.

    """
    try:
        serializer = serializers.UpdateSetSerializer(data=request.data)
        if serializer.is_valid():
            set_ = oai_provider_set_api.get_by_id(serializer.data.get('set_id'))
            serializer.update(set_, serializer.data)
            oai_provider_set_api.upsert(set_)
            content = OaiPmhMessage.get_message_labelled('Set updated with success.')

            return Response(content, status=status.HTTP_200_OK)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No Set found with the given id.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def delete_set(request):
    """ Delete a set by its id.

    POST http://<server_ip>:<server_port>/<rest_oai_pmh_url>/delete/set

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"set_id":"value"}

    """
    try:
        serializer = serializers.SetIdSerializer(data=request.data)
        if serializer.is_valid():
            set_ = oai_provider_set_api.get_by_id(serializer.data.get('set_id'))
            oai_provider_set_api.delete(set_)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        content = OaiPmhMessage.get_message_labelled('Set {0} deleted'
                                                     ' with success.'.format(set_.set_spec))

        return Response(content, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No Set found with the given id.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
