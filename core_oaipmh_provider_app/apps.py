""" Apps file for setting oai-pmh when app is ready
"""

import sys

from django.apps import AppConfig

from core_main_app.commons.exceptions import CoreError
from core_main_app.settings import (
    CAN_SET_PUBLIC_DATA_TO_PRIVATE,
    CAN_SET_WORKSPACE_PUBLIC,
    CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT,
)


class ProviderAppConfig(AppConfig):
    """Core application settings"""

    name = "core_oaipmh_provider_app"
    verbose_name = "Core OAI-PMH Provider App"

    def ready(self):
        """Run when the app is ready

        Returns:

        """
        if "migrate" not in sys.argv:
            from core_main_app.utils.migrations import ensure_migration_applied
            import core_oaipmh_provider_app.components.oai_provider_metadata_format.discover as discover_metadata_formats
            import core_oaipmh_provider_app.components.oai_settings.discover as discover_settings
            from core_oaipmh_provider_app.components.oai_data import (
                watch as data_watch,
            )
            from core_oaipmh_provider_app.tasks import insert_data_in_oai_data

            # Check if the system is using the correct settings
            _check_settings(
                CAN_SET_PUBLIC_DATA_TO_PRIVATE,
                CAN_SET_WORKSPACE_PUBLIC,
                CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT,
            )

            ensure_migration_applied(
                "core_oaipmh_provider_app", "0003_oai_data_bulk_delete"
            )

            discover_settings.init()
            discover_metadata_formats.init()
            insert_data_in_oai_data()

            data_watch.init()


def _check_settings(
    can_set_public_data_to_private,
    can_set_workspace_public,
    can_anonymous_access_public_document,
):
    """Check if the system is using the correct settings.

    Args:
        can_set_public_data_to_private:
        can_set_workspace_public:
        can_anonymous_access_public_document:

    Returns:

    """
    if (
        can_set_public_data_to_private
        or can_set_workspace_public
        or not can_anonymous_access_public_document
    ):
        raise CoreError(
            "The OAI-PMH provider app will only work for systems where "
            "CAN_SET_PUBLIC_DATA_TO_PRIVATE is set to False (published data cannot be unpublished) "
            "CAN_SET_WORKSPACE_PUBLIC is set to False "
            "(the global public workspace is used for all published data) "
            "and CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT is set to True "
            "(users that are not logged in can see published data)."
        )
