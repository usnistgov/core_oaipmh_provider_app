""" OAI-Provider System API
"""
from core_main_app.utils.xml import is_schema_valid


def upsert_oai_provider_metadata_format(oai_provider_metadata_format):
    """Create or update an OaiProviderMetadataFormat.

    Args:
        oai_provider_metadata_format: OaiProviderMetadataFormat to create or update.

    Returns:
        OaiProviderMetadataFormat instance.


    """
    is_schema_valid(oai_provider_metadata_format.xml_schema)
    return oai_provider_metadata_format.save_object()
