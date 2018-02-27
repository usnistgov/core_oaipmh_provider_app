""" OaiProviderSet rest api
"""

from core_oaipmh_common_app.commons import exceptions as exceptions_oai
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import core_oaipmh_provider_app.components.oai_provider_set.api as oai_provider_set_api
from core_main_app.commons import exceptions
from core_main_app.utils.decorators import api_staff_member_required
from core_oaipmh_provider_app.rest import serializers


class SetsList(APIView):
    @method_decorator(api_staff_member_required())
    def get(self, request):
        """ Return all sets.

        GET http://<server_ip>:<server_port>/<rest_oai_pmh_url>/set

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

    @method_decorator(api_staff_member_required())
    def post(self, request):
        """ Add a new set.

        POST http://<server_ip>:<server_port>/<rest_oai_pmh_url>/set

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
            # Build serializer
            serializer = serializers.OaiProviderSetSerializer(data=request.data)
            # Validate data
            serializer.is_valid(True)
            # Save data
            serializer.save()
            content = OaiPmhMessage.get_message_labelled('Set added with success.')

            return Response(content, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = OaiPmhMessage.get_message_labelled(validation_exception.detail)
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions_oai.OAIAPIException as e:
            return e.response()
        except Exception as e:
            content = OaiPmhMessage.get_message_labelled(e.message)
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SetDetail(APIView):
    @method_decorator(api_staff_member_required())
    def get(self, request, set_id):
        """ Get a set by its id.

        GET http://<server_ip>:<server_port>/<rest_oai_pmh_url>/set/{id}

        Params:
            request (HttpRequest): request.

        Returns:
            Response object.

        """
        try:
            set_ = oai_provider_set_api.get_by_id(set_id)
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

    @method_decorator(api_staff_member_required())
    def delete(self, request, set_id):
        """ Delete a set by its id.

        DELETE http://<server_ip>:<server_port>/<rest_oai_pmh_url>/set/{id}

        Args:
            request (HttpRequest): request.

        Returns:
            Response object.

        """
        try:
            set_ = oai_provider_set_api.get_by_id(set_id)
            oai_provider_set_api.delete(set_)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.DoesNotExist:
            content = OaiPmhMessage.get_message_labelled('No Set found with the given id.')
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as e:
            return e.response()
        except Exception as e:
            content = OaiPmhMessage.get_message_labelled(e.message)
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @method_decorator(api_staff_member_required())
    def patch(self, request, set_id):
        """ Update set.

        PATCH http://<server_ip>:<server_port>/<rest_oai_pmh_url>/set/{id}

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
            set_ = oai_provider_set_api.get_by_id(set_id)
            # Build serializer
            serializer = serializers.OaiProviderSetSerializer(instance=set_, data=request.data)
            # Validate data
            serializer.is_valid(True)
            # Save data
            serializer.save()
            content = OaiPmhMessage.get_message_labelled('Set updated with success.')

            return Response(content, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = OaiPmhMessage.get_message_labelled(validation_exception.detail)
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = OaiPmhMessage.get_message_labelled('No Set found with the given id.')
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as e:
            return e.response()
        except Exception as e:
            content = OaiPmhMessage.get_message_labelled(e.message)
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
