""" discover Data for oai-pmh
"""
import json
import logging

from celery import shared_task, current_app
from django.core import serializers

from core_main_app.system import api as data_system_api
from core_oaipmh_provider_app.components.oai_data import api as oai_data_api
from core_oaipmh_provider_app.components.oai_settings import (
    api as oai_settings_api,
)

logger = logging.getLogger(__name__)


def insert_data_in_oai_data():
    """Insert XML data into OAI Data to allow for harvesting.

    Launch an asynchronous task when the server is starting.

    Returns:
    """
    if current_app.backend.is_async:
        insert_data_task.apply_async()
    else:
        logger.warning(
            "Task 'insert_data_task' has been disabled since broker has no async "
            "capabilities"
        )


@shared_task(name="insert_data_task")
def insert_data_task():
    """Insert XML data into OAI Data to allow for harvesting."""
    logger.info("START OAI Data discovery...")

    # Exit early if harvesting is disable
    oai_settings = oai_settings_api.get()
    if not oai_settings.enable_harvesting:
        logger.info("Harvesting OFF. Exiting discovery...")
        return

    try:
        # Retrieve the Data ids in OAI Data
        oai_data = oai_data_api.get_all()
        oai_data_ids = serializers.serialize("json", oai_data.only("data"))
        registered_data_id = [
            data["fields"]["data"] for data in json.loads(oai_data_ids)
        ]

        # Retrieve all data not registered in OAI and insert them in OAI data
        data = data_system_api.get_all_except(registered_data_id)
        logger.debug("XML Data retrieved.")

        for document in data:
            oai_data_api.upsert_from_data(document, force_update=False)

        logger.debug("OAI Data inserted.")
    except Exception as exception:
        logger.error("Impossible to init the OAI-PMH data: %s", str(exception))

    logger.info("OAI Data discovery done")
