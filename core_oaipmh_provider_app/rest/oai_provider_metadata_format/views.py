""" OaiProviderMetadataFormat rest api
"""
from core_main_app.commons import exceptions
from core_main_app.utils.decorators import api_staff_member_required
from core_oaipmh_provider_app.components.oai_provider_metadata_format import api as oai_provider_metadata_format_api
from core_main_app.components.template import api as oai_template_api
from core_main_app.components.xsl_transformation import api as oai_xslt_api
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from core_oaipmh_common_app.commons import exceptions as exceptions_oai
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from core_oaipmh_provider_app.rest import serializers
from core_oaipmh_provider_app.components.oai_xsl_template.models import OaiXslTemplate
from core_oaipmh_provider_app.components.oai_xsl_template import api as  oai_xsl_template_api


@api_view(['GET'])
@api_staff_member_required()
def select_metadata_format(request):
    """ Get a metadata format by its id.

    GET http://<server_ip>:<server_port>/<rest_oai_pmh_url>/select/metadata_format

    Params:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"metadata_format_id":"value"}

    Raises:
        OAIAPISerializeLabelledException: Serialization error.

    """
    try:
        serializer = serializers.MetadataFormatIdSerializer(data=request.query_params)
        if serializer.is_valid():
            metadata_format = oai_provider_metadata_format_api.get_by_id(serializer.data.get('metadata_format_id'))
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        serializer = serializers.OaiProviderMetadataFormatSerializer(metadata_format)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No Metadata Format found with the given id.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@api_staff_member_required()
def select_all_metadata_formats(request):
    """ Return all metadata formats.

    GET http://<server_ip>:<server_port>/<rest_oai_pmh_url>/select/all/metadata_formats

    Returns:
        Response object.

    """
    try:
        metadata_formats = oai_provider_metadata_format_api.get_all()
        serializer = serializers.OaiProviderMetadataFormatSerializer(metadata_formats, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def add_metadata_format(request):
    """ Add a new metadata format.

    POST http://<server_ip>:<server_port>/<rest_oai_pmh_url>/add/metadata_format

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"metadata_prefix":"value","schema":"URL"}

    Raises:
        OAIAPISerializeLabelledException: Serialization error.

    """
    try:
        serializer = serializers.AddMetadataFormatSerializer(data=request.data)
        if serializer.is_valid():
            metadata_prefix = serializer.data.get('metadata_prefix')
            schema = serializer.data.get('schema')
            return oai_provider_metadata_format_api.add_metadata_format(metadata_prefix, schema)
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
def add_template_metadata_format(request):
    """ Add a new template as metadata format.

    POST http://<server_ip>:<server_port>/<rest_oai_pmh_url>/add/template_metadata_format

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"metadata_prefix":"value","template_id":"value"}

    Raises:
        OAIAPISerializeLabelledException: Serialization error.

    """
    try:
        serializer = serializers.AddTemplateMetadataFormatSerializer(data=request.data)
        if serializer.is_valid():
            metadata_prefix = serializer.data.get('metadata_prefix')
            template_id = serializer.data.get('template_id')
            return oai_provider_metadata_format_api.add_template_metadata_format(metadata_prefix, template_id)
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
def delete_metadata_format(request):
    """ Delete a metadata format by its id.

    POST http://<server_ip>:<server_port>/<rest_oai_pmh_url>/delete/metadata_format

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"metadata_format_id":"value"}

    """
    try:
        serializer = serializers.MetadataFormatIdSerializer(data=request.data)
        if serializer.is_valid():
            metadata_format = oai_provider_metadata_format_api.get_by_id(serializer.data.get('metadata_format_id'))
            oai_provider_metadata_format_api.delete(metadata_format)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        content = OaiPmhMessage.get_message_labelled('Metadata Format {0} deleted'
                                                     ' with success.'.format(metadata_format.metadata_prefix))

        return Response(content, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No Metadata Format found with the given id.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@api_staff_member_required()
def update_metadata_format(request):
    """ Update a metadata format.

    PUT http://<server_ip>:<server_port>/<rest_oai_pmh_url>/update/metadata_format

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"metadata_format_id":"value", "metadata_prefix":"value"}

    """
    try:
        serializer = serializers.UpdateMetadataFormatSerializer(data=request.data)
        if serializer.is_valid():
            metadata_format = oai_provider_metadata_format_api.get_by_id(serializer.data.get('metadata_format_id'))
            serializer.update(metadata_format, serializer.data)
            oai_provider_metadata_format_api.upsert(metadata_format)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
        content = OaiPmhMessage.get_message_labelled('Metadata Format updated with success.')

        return Response(content, status=status.HTTP_200_OK)
    except exceptions.DoesNotExist:
        content = OaiPmhMessage.get_message_labelled('No Metadata Format found with the given id.')
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def template_to_metadata_format_mapping_xslt(request):
    """ Map a template, a metadata format and a XSLT. Used for the transformation of the template toward the
        metadata format thanks to the XSLT.

    POST http://<server_ip>:<server_port>/<rest_oai_pmh_url>/mapping/template/metadata_format/xslt

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"template_id": "value", "metadata_format_id": "value", "xslt_id": "value"}

    """
    try:
        serializer = serializers.TemplateToMFMappingXSLTSerializer(data=request.data)
        if serializer.is_valid():
            # Get objects
            template = oai_template_api.get(serializer.data.get('template_id'))
            xslt = oai_xslt_api.get_by_id(serializer.data.get('xslt_id'))
            metadata_format = oai_provider_metadata_format_api.get_by_id(serializer.data.get('metadata_format_id'))
            # Check if the given metadata format is a template metadata format
            if metadata_format.is_template:
                raise exceptions_oai.\
                    OAIAPILabelledException(message="Impossible to map a XSLT to a template metadata format",
                                            status_code=status.HTTP_400_BAD_REQUEST)
            try:
                oai_xsl_template = oai_xsl_template_api.get_by_template_id_and_metadata_format_id(template.id,
                                                                                                  metadata_format.id)
                oai_xsl_template.xslt = xslt
            except exceptions.DoesNotExist as e:
                oai_xsl_template = OaiXslTemplate(oai_metadata_format=metadata_format, template=template, xslt=xslt)

            oai_xsl_template_api.upsert(oai_xsl_template)
            content = OaiPmhMessage.get_message_labelled('Mapping configured with success.')

            return Response(content, status=status.HTTP_200_OK)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
    except exceptions.DoesNotExist as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@api_staff_member_required()
def template_to_metadata_format_unmapping_xslt(request):
    """ Remove the mapping between a template, a metadata format and a XSLT.

    POST http://<server_ip>:<server_port>/<rest_oai_pmh_url>/unmapping/template/metadata_format/xslt

    Args:
        request (HttpRequest): request.

    Returns:
        Response object.

    Examples:
        >>> {"template_id": "value", "metadata_format_id": "value"}

    """
    try:
        serializer = serializers.TemplateToMFUnMappingXSLTSerializer(data=request.data)
        if serializer.is_valid():
            # Get template id
            template_id = serializer.data.get('template_id')
            # Get metadata format id
            metadata_format_id = serializer.data.get('metadata_format_id')
            # Get mapping
            oai_xsl_template = oai_xsl_template_api.get_by_template_id_and_metadata_format_id(template_id,
                                                                                              metadata_format_id)
            # Delete the mapping
            oai_xsl_template_api.delete(oai_xsl_template)
            content = OaiPmhMessage.get_message_labelled('Mapping deleted with success.')

            return Response(content, status=status.HTTP_200_OK)
        else:
            raise exceptions_oai.OAIAPISerializeLabelledException(errors=serializer.errors,
                                                                  status_code=status.HTTP_400_BAD_REQUEST)
    except exceptions.DoesNotExist as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    except exceptions_oai.OAIAPIException as e:
        return e.response()
    except Exception as e:
        content = OaiPmhMessage.get_message_labelled(e.message)
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
