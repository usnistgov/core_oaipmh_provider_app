""" Apps file for setting oai-pmh when app is ready
"""
from django.apps import AppConfig

import core_oaipmh_provider_app.components.oai_provider_metadata_format.discover as discover_metadata_formats
import core_oaipmh_provider_app.components.oai_settings.discover as discover_settings
import core_oaipmh_provider_app.components.oai_data.discover as discover_data
from core_oaipmh_provider_app.components.oai_data import watch as data_watch


class ProviderAppConfig(AppConfig):
    """ Core application settings
    """
    name = 'core_oaipmh_provider_app'

    def ready(self):
        """ Run when the app is ready

        Returns:

        """
        discover_settings.init()
        discover_metadata_formats.init()
        discover_data.check_data_info()

        data_watch.init()
