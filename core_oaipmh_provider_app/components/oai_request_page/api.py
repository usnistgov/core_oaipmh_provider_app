""" OAIRequestPage API calls
"""
import logging
import random
import string

from core_main_app.commons import exceptions
from core_oaipmh_provider_app.commons import constants
from core_oaipmh_provider_app.components.oai_request_page.models import \
    OaiRequestPage

logger = logging.getLogger(__name__)


def get_by_resumption_token(resumption_token):
    """ Get request information using resumption token

    Args:
        resumption_token:

    Returns:
    """
    return OaiRequestPage.get_by_resumption_token(resumption_token)


def upsert(oai_request_page_object):
    """ Insert or update a given OAIRequestPage object

    Args:
        oai_request_page_object:

    Returns:
    """
    def _generate_token(token_length=16):
        """ Generate a random token of a given length.

        Args:
            token_length:

        Raises:
            ApiError:

        Returns:
        """
        return ''.join(
            random.choice(string.ascii_lowercase + string.digits)
            for _ in range(token_length)
        )

    # Loop until OAIRequestPage object is inserted or raise exception if the
    # maximum retry is reached.
    for _ in range(constants.MAX_INSERT_RETRIES):
        try:
            oai_request_page_object.resumption_token = _generate_token()
            return oai_request_page_object.save()
        except Exception as e:
            logger.warning(
                "Error while saving OAIRequestPage object: %s" % str(e)
            )

    raise exceptions.ApiError("Exceeded number of tries to save OAIRequestPage")



