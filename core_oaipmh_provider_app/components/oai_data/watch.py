"""
Handle signals.
"""
import logging

from django.db.models.signals import post_save, pre_delete

from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_main_app.utils.datetime import datetime_now
from core_oaipmh_provider_app.commons import status
from core_oaipmh_provider_app.components.oai_data import api as oai_data_api

logger = logging.getLogger(__name__)


def init():
    """Connect to Data object events."""
    post_save.connect(post_save_data, sender=Data)
    pre_delete.connect(pre_delete_data, sender=Data)


def post_save_data(sender, instance, **kwargs):
    """Method executed after saving a Data object.
    Args:
        sender: Class.
        instance: Data.
        **kwargs: Args.

    """
    oai_data_api.upsert_from_data(instance, force_update=True)


def pre_delete_data(sender, instance, **kwargs):
    """Method executed before deleting a Data object.
    Args:
        sender: Class.
        instance: Data.
        **kwargs: Args.

    """
    try:
        oai_data = oai_data_api.get_by_data(instance)
        oai_data.oai_date_stamp = datetime_now()
        oai_data.status = status.DELETED

        oai_data_api.upsert(oai_data)
    except exceptions.DoesNotExist:
        logger.warning(
            "pre_delete_data: no oai data found for the given document: %s",
            str(instance.pk),
        )
    except Exception as exception:
        logger.warning(
            "pre_delete_data threw an exception: %s", str(exception)
        )
