"""
OaiProviderMetadataFormat API
"""
from core_main_app.components.template import api as template_api
from core_main_app.commons.exceptions import DoesNotExist
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import OaiProviderMetadataFormat
from core_oaipmh_common_app.commons import exceptions as oai_pmh_exceptions
from core_oaipmh_common_app.commons.messages import OaiPmhMessage
from xml_utils.xsd_tree.xsd_tree import XSDTree
import xml_utils.commons.exceptions as exceptions
from rest_framework.response import Response
from rest_framework import status
import requests


def upsert(oai_provider_metadata_format):
    """ Create or update an OaiProviderMetadataFormat.

    Args:
        oai_provider_metadata_format: OaiProviderMetadataFormat to create or update.

    Returns:
        OaiProviderMetadataFormat instance.


    """
    return oai_provider_metadata_format.save()


def delete(oai_provider_metadata_format):
    """ Delete an OaiProviderMetadataFormat.

    Args:
        oai_provider_metadata_format: OaiProviderMetadataFormat to delete.

    """
    oai_provider_metadata_format.delete()


def get_by_id(oai_provider_metadata_format_id):
    """ Get an OaiProviderMetadataFormat by its id.

    Args:
        oai_provider_metadata_format_id: Id of the OaiProviderMetadataFormat.

    Returns:
        OaiProviderMetadataFormat instance.

    """
    return OaiProviderMetadataFormat.get_by_id(oai_metadata_format_id=oai_provider_metadata_format_id)


def get_by_metadata_prefix(metadata_prefix):
    """ Get an OaiProviderMetadataFormat by its metadata prefix.

    Args:
        metadata_prefix: metadata_prefix of the OaiProviderMetadataFormat.

    Returns:
        OaiProviderMetadataFormat instance.

    """
    return OaiProviderMetadataFormat.get_by_metadata_prefix(metadata_prefix=metadata_prefix)


def get_all():
    """ Get all OaiProviderMetadataFormat.

    Returns:
        List of OaiProviderMetadataFormat.

    """
    return OaiProviderMetadataFormat.get_all()


def get_all_custom_metadata_format(order_by_field=None):
    """ Get all custom OaiProviderMetadataFormat.

    Args:
        order_by_field: Order by field.

    Returns:
        List of metadata format.

    """
    return OaiProviderMetadataFormat.get_all_custom_metadata_format(order_by_field)


def get_all_default_metadata_format(order_by_field=None):
    """ Get all default OaiProviderMetadataFormat.

    Args:
        order_by_field: Order by field.

    Returns:
        List of metadata format.

    """
    return OaiProviderMetadataFormat.get_all_default_metadata_format(order_by_field)


def get_all_template_metadata_format(order_by_field=None):
    """ Get all OaiProviderMetadataFormat based on a template.

    Args:
        order_by_field: Order by field.

    Returns:
        List of metadata format.

    """
    return OaiProviderMetadataFormat.get_all_template_metadata_format(order_by_field)


def get_all_no_template_metadata_format():
    """ Get all OaiProviderMetadataFormat except the metadata formats based on a template.

     Returns:
         List of metadata format.

     """
    return OaiProviderMetadataFormat.get_all_no_template_metadata_format()


def get_all_by_templates(templates):
    """ Get all OaiProviderMetadataFormat used by a list of templates.

    Returns:
        List of metadata format.

    """
    return OaiProviderMetadataFormat.get_all_by_templates(templates)


def add_metadata_format(metadata_prefix, schema_url):
    """ Add a new metadata format.
    Args:
        metadata_prefix: Metadata Prefix.
        schema_url: URL of the schema.

    Returns: Response.

    """
    try:
        http_response = requests.get(schema_url)
        if http_response.status_code == status.HTTP_200_OK:
            xml_schema = http_response.text
            target_namespace = _get_target_namespace(xml_schema)
            obj = OaiProviderMetadataFormat(metadata_prefix=metadata_prefix, schema=schema_url, xml_schema=xml_schema,
                                            metadata_namespace=target_namespace, is_default=False, is_template=False)
            upsert(obj)
            content = OaiPmhMessage.get_message_labelled('Metadata format added with success.')

            return Response(content, status=status.HTTP_201_CREATED)
        else:
            raise oai_pmh_exceptions.OAIAPILabelledException(message='Unable to add the new metadata format. Impossible'
                                                                     ' to retrieve the schema at the given URL',
                                                             status_code=status.HTTP_400_BAD_REQUEST)
    except exceptions.XMLError as e:
        raise oai_pmh_exceptions.OAIAPILabelledException(message='Unable to add the new metadata format.%s' % e.message,
                                                         status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise oai_pmh_exceptions.OAIAPILabelledException(message='Unable to add the new metadata format.%s' % e.message,
                                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def add_template_metadata_format(metadata_prefix, template_id):
    """ Add a new template metadata format.
    Args:
        metadata_prefix: Metadata Prefix.
        template_id: Id of the template.

    Returns: Response.

    """
    try:
        template = template_api.get(template_id)
        xml_schema = template.content
        target_namespace = _get_target_namespace(xml_schema)
        # FIXME: Once the server is developed
        schema_url = ""  # OAI_HOST_URI + reverse('getXSD', args=[template.filename])
        obj = OaiProviderMetadataFormat(metadata_prefix=metadata_prefix, schema=schema_url, xml_schema=xml_schema,
                                        metadata_namespace=target_namespace, is_default=False, is_template=True,
                                        template=template)
        upsert(obj)
        content = OaiPmhMessage.get_message_labelled('Metadata format added with success.')

        return Response(content, status=status.HTTP_201_CREATED)
    except oai_pmh_exceptions.OAIAPILabelledException as e:
        raise e
    except DoesNotExist:
        raise oai_pmh_exceptions.OAIAPILabelledException(message='Unable to add the new metadata format. '
                                                                 'Impossible to retrieve the template with the '
                                                                 'given template',
                                                         status_code=status.HTTP_404_NOT_FOUND)
    except exceptions.XMLError as e:
        raise oai_pmh_exceptions.OAIAPILabelledException(message='Unable to add the new metadata format.%s' % e.message,
                                                         status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        raise oai_pmh_exceptions.OAIAPILabelledException(message='Unable to add the new metadata format.%s' % e.message,
                                                         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_target_namespace(xml_schema):
    """ Get the target namespace.
    Args:
        xml_schema:  XML representation of the schema.

    Returns:
        The target namespace.

    """
    xsd_tree = XSDTree.fromstring(xml_schema.encode('utf-8'))
    root = xsd_tree.find(".")
    if 'targetNamespace' in root.attrib:
        target_namespace = root.attrib['targetNamespace']
        if target_namespace not in root.nsmap.values():
            message = "The use of a targetNamespace without an associated prefix is not supported."
            raise oai_pmh_exceptions.OAIAPILabelledException(message=message,
                                                             status_code=status.HTTP_400_BAD_REQUEST)
    else:
        target_namespace = "http://www.w3.org/2001/XMLSchema"

    return target_namespace
