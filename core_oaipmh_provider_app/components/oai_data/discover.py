""" discover Data for oai-pmh
"""
import logging

from core_oaipmh_provider_app.components.oai_data import api as oai_data_api
from core_main_app.components.data.models import Data

logger = logging.getLogger(__name__)


def check_data_info():
    """ Check OAI-PMH data information.
    """
    logger.info("START oai data discovery.")

    try:
        data = Data.get_all()
        logger.debug("XML Data retrieved.")

        for document in data:
            oai_data_api.upsert_from_data(document, force_update=False)

        logger.debug("OAI Data inserted.")
    except Exception, e:
        logger.error("Impossible to init the OAI-PMH data: %s" % e.message)

    logger.info("FINISH oai data discovery.")
