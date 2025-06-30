""" OaiProviderSet rest api
"""

from django.utils.decorators import method_decorator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

import core_oaipmh_provider_app.components.oai_provider_set.api as oai_provider_set_api
from core_main_app.commons import exceptions
from core_main_app.utils.decorators import api_staff_member_required
from core_oaipmh_common_app.commons import exceptions as exceptions_oai
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from core_oaipmh_provider_app.rest import serializers
from core_oaipmh_provider_app.rest.serializers import (
    OaiProviderSetListSerializer,
    OaiProviderSetCreateUpdateSerializer,
)


@extend_schema(
    tags=["OAI Provider Set"],
    description="Sets List",
)
class SetsList(APIView):
    """Sets List"""

    @extend_schema(
        summary="Get all OaiProviderSet",
        description="Get all OaiProviderSet",
        responses={
            200: OaiProviderSetListSerializer(many=True),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def get(self, request):
        """Get all OaiProviderSet
        Args:
            request: HTTP request
        Returns:
            - code: 200
              content: List of OaiProviderSet
            - code: 500
              content: Internal server error
        """
        try:
            sets = oai_provider_set_api.get_all()
            serializer = serializers.OaiProviderSetListSerializer(
                sets, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Create a OaiProviderSet",
        description="Create a OaiProviderSet",
        request=OaiProviderSetCreateUpdateSerializer,
        responses={
            201: OpenApiResponse(description="Success Label"),
            400: OpenApiResponse(description="Validation error"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def post(self, request):
        """Create a OaiProviderSet
        Parameters:
            {
              "set_spec": "value",
              "set_name":"value",
              "templates_manager": ["id1", "id2"],
              "description":"value"
            }
        Args:
            request: HTTP request
        Returns:
            - code: 201
              content: Success Label
            - code: 400
              content: Validation error
            - code: 500
              content: Internal server error
        """
        try:
            # Build serializer
            serializer = serializers.OaiProviderSetCreateUpdateSerializer(
                data=request.data, context={"request": request}
            )
            # Validate data
            serializer.is_valid(raise_exception=True)
            # Save data
            serializer.save()
            content = OaiPmhMessage.get_message_labelled("Set added.")
            return Response(content, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = OaiPmhMessage.get_message_labelled(
                validation_exception.detail
            )
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["OAI Provider Set"],
    description="Set Detail",
)
class SetDetail(APIView):
    """Set Detail"""

    @extend_schema(
        summary="Get a OaiProviderSet",
        description="Get a OaiProviderSet",
        parameters=[
            OpenApiParameter(
                name="set_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="OaiProviderSet ID",
            ),
        ],
        responses={
            200: OaiProviderSetListSerializer,
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def get(self, request, set_id):
        """Get a OaiProviderSet
        Args:
            request: HTTP request
            set_id: ObjectId
        Returns:
            - code: 200
              content: Registry
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            set_ = oai_provider_set_api.get_by_id(set_id)
            serializer = serializers.OaiProviderSetListSerializer(
                set_, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except exceptions.DoesNotExist:
            content = OaiPmhMessage.get_message_labelled(
                "No Set found with the given id."
            )
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Delete a OaiProviderSet",
        description="Delete a OaiProviderSet",
        parameters=[
            OpenApiParameter(
                name="set_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="OaiProviderSet ID",
            ),
        ],
        responses={
            204: OpenApiResponse(description="Deletion succeed"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def delete(self, request, set_id):
        """Delete a OaiProviderSet
        Args:
            request: HTTP request
            set_id: ObjectId
        Returns:
            - code: 204
              content: Deletion succeed
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            set_ = oai_provider_set_api.get_by_id(set_id)
            oai_provider_set_api.delete(set_)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except exceptions.DoesNotExist:
            content = OaiPmhMessage.get_message_labelled(
                "No Set found with the given id."
            )
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Update a OaiProviderSet",
        description="Update a OaiProviderSet",
        parameters=[
            OpenApiParameter(
                name="set_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="OaiProviderSet ID",
            ),
        ],
        request=OaiProviderSetCreateUpdateSerializer,
        responses={
            200: OpenApiResponse(description="Success message"),
            400: OpenApiResponse(description="Validation error"),
            404: OpenApiResponse(description="Object was not found"),
            500: OpenApiResponse(description="Internal server error"),
        },
    )
    @method_decorator(api_staff_member_required())
    def patch(self, request, set_id):
        """Update a OaiProviderSet
        Parameters:
            {
              "set_spec":"value",
              "set_name":"value",
              "templates_manager": ["id1", "id2"],
              "description":"value"
            }
        Args:
            request: HTTP request
            set_id:
        Returns:
            - code: 200
              content: Success message
            - code: 400
              content: Validation error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            set_ = oai_provider_set_api.get_by_id(set_id)
            # Build serializer
            serializer = serializers.OaiProviderSetCreateUpdateSerializer(
                instance=set_,
                data=request.data,
                context={"request": request},
            )
            # Validate data
            serializer.is_valid(raise_exception=True)
            # Save data
            serializer.save()
            content = OaiPmhMessage.get_message_labelled("Set updated.")
            return Response(content, status=status.HTTP_200_OK)
        except ValidationError as validation_exception:
            content = OaiPmhMessage.get_message_labelled(
                validation_exception.detail
            )
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = OaiPmhMessage.get_message_labelled(
                "No Set found with the given id."
            )
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except exceptions_oai.OAIAPIException as exception:
            return exception.response()
        except Exception as exception:
            content = OaiPmhMessage.get_message_labelled(str(exception))
            return Response(
                content, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
