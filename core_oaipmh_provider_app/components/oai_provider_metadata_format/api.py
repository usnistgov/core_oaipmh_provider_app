"""
OaiProviderMetadataFormat API
"""

from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import OaiProviderMetadataFormat


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
