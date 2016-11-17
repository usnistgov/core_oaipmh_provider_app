"""
OaiProviderMetadataFormat API
"""

from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import OaiProviderMetadataFormat
from core_main_app.commons import exceptions


def upsert(oai_provider_metadata_format):
    """ Create or update an OaiProviderMetadataFormat.

        Parameters:
            oai_provider_metadata_format: OaiProviderMetadataFormat to create or update.

        Returns:
            OaiProviderMetadataFormat instance.

        Raises:
            ApiError: If the save operation failed.

    """
    try:
        return oai_provider_metadata_format.save()
    except Exception as e:
        raise exceptions.ApiError('Save OaiProviderMetadataFormat failed: {0}.'.format(e.message))


def delete(oai_provider_metadata_format):
    """ Delete an OaiProviderMetadataFormat.

        Parameters:
            oai_provider_metadata_format: OaiProviderMetadataFormat to delete.

        Raises:
            ApiError: If the delete operation failed.

    """
    try:
        oai_provider_metadata_format.delete()
    except Exception as e:
        raise exceptions.ApiError('Impossible to delete OaiProviderMetadataFormat.: {0}.'.format(e.message))


def get_by_id(oai_provider_metadata_format_id):
    """ Get an OaiProviderMetadataFormat by its id.

        Parameters:
            oai_provider_metadata_format_id: Id of the OaiProviderMetadataFormat.

        Returns:
            OaiProviderMetadataFormat instance.

        Raises:
            ApiError: OaiProviderMetadataFormat could not be found.

    """
    try:
        return OaiProviderMetadataFormat.get_by_id(oai_metadata_format_id=oai_provider_metadata_format_id)
    except:
        raise exceptions.ApiError('No OaiProviderMetadataFormat could be found with the given id.')


def get_by_metadata_prefix(metadata_prefix):
    """ Get an OaiProviderMetadataFormat by its metadata prefix.

        Parameters:
            metadata_prefix: metadata_prefix of the OaiProviderMetadataFormat.

        Returns:
            OaiProviderMetadataFormat instance.

        Raises:
            ApiError: OaiProviderMetadataFormat could not be found.

    """
    try:
        return OaiProviderMetadataFormat.get_by_metadata_prefix(metadata_prefix=metadata_prefix)
    except:
        raise exceptions.ApiError('No OaiProviderMetadataFormat could be found with the given metadata prefix.')


def get_all():
    """ Get all OaiProviderMetadataFormat.

        Returns:
            List of OaiProviderMetadataFormat.

    """
    return OaiProviderMetadataFormat.get_all()


def get_all_custom_metadata_format():
    """ Get all custom OaiProviderMetadataFormat.

        Returns:
            List of metadata format.

    """
    return OaiProviderMetadataFormat.get_all_custom_metadata_format()


def get_all_default_metadata_format():
    """ Get all default OaiProviderMetadataFormat.

        Returns:
            List of metadata format.

    """
    return OaiProviderMetadataFormat.get_all_default_metadata_format()


def get_all_template_metadata_format():
    """ Get all OaiProviderMetadataFormat based on a template.

        Returns:
            List of metadata format.

    """
    return OaiProviderMetadataFormat.get_all_template_metadata_format()


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
