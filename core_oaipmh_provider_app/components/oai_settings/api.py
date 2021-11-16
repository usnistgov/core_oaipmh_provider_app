"""
OaiSettings API
"""


from core_oaipmh_provider_app.components.oai_settings.models import OaiSettings


def upsert(oai_settings):
    """Create or update an OaiSettings.

    Args:
        oai_settings: The OaiSettings to create or update.

    Returns: The OaiSettings instance.

    """
    oai_settings.save()
    return oai_settings


def get():
    """Get the settings.

    Returns:
        The OaiSettings instance.

    """
    return OaiSettings.get()
