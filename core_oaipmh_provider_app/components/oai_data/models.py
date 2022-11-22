"""
OaiData model
"""

import operator
from functools import reduce

from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from core_main_app.commons import exceptions
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template


class OaiData(models.Model):
    """Represents a data for Oai-Pmh Provider"""

    data = models.ForeignKey(
        Data, blank=False, null=True, on_delete=models.SET_NULL
    )
    oai_date_stamp = models.DateTimeField(blank=False, null=True, default=None)
    status = models.CharField(blank=False, max_length=200)
    template = models.ForeignKey(
        Template, blank=False, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        """Meta"""

        verbose_name = "Oai data"
        verbose_name_plural = "Oai data"

    @staticmethod
    def _filter_by_date(from_date, until_date):
        """Create Q query to filter between two dates

        Args:
            from_date:
            until_date:

        Returns:
            list - The query to be used to filter item between these dates
        """
        qlist = []

        if from_date:
            qlist.append(Q(oai_date_stamp__gte=from_date))

        if until_date:
            qlist.append(Q(oai_date_stamp__lte=until_date))

        return qlist

    @staticmethod
    def _filter_public_data():
        """Create Q query to output public data only

        Returns:
             list - Filters to only return public data
        """
        return [
            Q(data__workspace__isnull=False),
            Q(data__workspace__is_public=True),
        ]

    @staticmethod
    def get_by_id(oai_data_id):
        """Returns the object with the given id

        Args:
            oai_data_id:

        Returns:
            OaiData (obj): OaiData object with the given id

        Raises:
            DoesNotExist: The OaiData doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiData.objects.get(pk=str(oai_data_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_data(data):
        """Get an OaiData by its data.

        Args:
            data: Data instance.

        Returns:
            OaiData instance.

        Raises:
            DoesNotExist: The OaiData doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiData.objects.get(data=data)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_all():
        """Return all OaiData.

        Returns:
            List of OaiData.

        """
        return OaiData.objects.all()

    @staticmethod
    def get_all_by_data_list_and_timeframe(data_list, from_date, until_date):
        """Get all OaiData from a specific data list.

        Args:
            data_list: List of data.
            from_date: Timeframe start.
            until_date: Timeframe end.

        Returns:
            List of OaiData instance.
        """
        q_list = [Q(data__in=data_list)] + OaiData._filter_by_date(
            from_date, until_date
        )

        return OaiData.objects.filter(reduce(operator.and_, q_list)).all()

    @staticmethod
    def get_all_by_template_and_timeframe(template, from_date, until_date):
        """Get all OaiData used by a template.

        Args:
            template: The template.
            from_date:
            until_date:

        Returns:
            List of OaiData.

        """
        q_list = [Q(template=template)] + OaiData._filter_by_date(
            from_date, until_date
        )

        return OaiData.objects.filter(reduce(operator.and_, q_list)).all()

    @staticmethod
    def get_all_by_template_list_and_timeframe(
        template_list, from_date, until_date
    ):
        """Get all OaiData used by a list of templates.

        Args:
            template_list: List of templates.
            from_date:
            until_date:

        Returns:
            List of OaiData.

        """
        q_list = [Q(template__in=template_list)] + OaiData._filter_by_date(
            from_date, until_date
        )

        return OaiData.objects.filter(reduce(operator.and_, q_list)).all()

    @staticmethod
    def get_all_by_status(status):
        """Get all OaiData by their status.
        Args:
            status: Status.

        Returns:
            List of OaiData.

        """
        return OaiData.objects.filter(status=status).all()

    @staticmethod
    def get_earliest_data_date():
        """Get the earliest OaiData date
        Returns:
            Date of the earliest OaiData.

        """
        try:
            earliest_record = OaiData.objects.order_by(
                "oai_date_stamp"
            ).first()

            return earliest_record.oai_date_stamp
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    def __str__(self):
        """Return OAIData object as string

        Returns:

        """
        return f"{self.data.title if self.data else 'DELETED'} ({self.pk})"
