""" discover settings for oai-pmh
"""

import logging

from core_main_app.commons.exceptions import CoreError

logger = logging.getLogger(__name__)


def init():
    """Init settings for the OAI-PMH feature. Set the name, identifier and the
    harvesting information.
    """
    from core_main_app.commons import exceptions
    from core_oaipmh_provider_app import settings
    from core_oaipmh_provider_app.components.oai_settings import (
        api as oai_settings_api,
    )
    from core_oaipmh_provider_app.components.oai_settings.models import (
        OaiSettings,
    )

    # Check if OAI_ADMINS setting is set
    if not settings.OAI_ADMINS:
        raise CoreError(
            "The OAI-PMH provider app is improperly configured: OAI_ADMINS not set."
            "Please set OAI_ADMINS in the project settings "
            '(e.g. OAI_ADMINS = ["admin1@example.com", "admin2@example.com"])'
            "or using an environment variable "
            "(e.g. OAI_ADMINS=admin1@example.com,admin2@example.com). "
        )

    logger.info("START oai settings discovery.")

    try:
        # Get OAI-PMH settings information about this server
        oai_settings_api.get()
    except exceptions.DoesNotExist:
        oai_settings = OaiSettings(
            repository_name=settings.OAI_NAME,
            repository_identifier=settings.OAI_REPO_IDENTIFIER,
            enable_harvesting=settings.OAI_ENABLE_HARVESTING,
        )
        oai_settings_api.upsert(oai_settings)
    except Exception as exception:
        logger.error("Impossible to init the settings: %s", str(exception))

    logger.info("FINISH oai settings discovery.")
