""" Settings for core_oaipmh_provider_app

Settings with the following syntax can be overwritten at the project level:
SETTING_NAME = getattr(settings, "SETTING_NAME", "Default Value")
"""
from os.path import dirname, realpath

from django.conf import settings

if not settings.configured:
    settings.configure()

INSTALLED_APPS = getattr(settings, "INSTALLED_APPS", [])

OAI_PROVIDER_ROOT = dirname(realpath(__file__))

# core_website_app settings
SERVER_URI = getattr(settings, "SERVER_URI", "")
CUSTOM_NAME = getattr(settings, "CUSTOM_NAME", "")

# core_explore_common_app settings
RESULTS_PER_PAGE = getattr(settings, "RESULTS_PER_PAGE", 10)

# OAI_PMH parameters
OAI_ADMINS = (("Administrator", "admin@example.com"),)
OAI_HOST_URI = SERVER_URI
OAI_NAME = CUSTOM_NAME + " OAI-PMH Server"
OAI_DELIMITER = ":"
OAI_DESCRIPTION = "OAI-PMH " + CUSTOM_NAME
OAI_GRANULARITY = "YYYY-MM-DDThh:mm:ssZ"  # the finest harvesting granularity supported by the repository
OAI_PROTOCOL_VERSION = "2.0"  # the version of the OAI-PMH supported by the repository
OAI_SCHEME = "oai"
OAI_REPO_IDENTIFIER = "server-x"
OAI_SAMPLE_IDENTIFIER = (
    OAI_SCHEME
    + OAI_DELIMITER
    + OAI_REPO_IDENTIFIER
    + OAI_DELIMITER
    + "id/12345678a123aff6ff5f2d9e"
)
OAI_DELETED_RECORD = "persistent"  # no; transient; persistent
OAI_ENABLE_HARVESTING = getattr(settings, "OAI_ENABLE_HARVESTING", False)

CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT = getattr(
    settings, "CAN_ANONYMOUS_ACCESS_PUBLIC_DOCUMENT", False
)
""" :py:class:`bool`: Can anonymous user access public document.
"""
