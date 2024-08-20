"""
OaiProviderSet model
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_oaipmh_common_app.components.oai_set.models import OaiSet


class OaiProviderSet(OaiSet):
    """Represents a set for Oai-Pmh Provider"""

    templates_manager = models.ManyToManyField(TemplateVersionManager)
    description = models.TextField(blank=True)

    @staticmethod
    def get_by_id(oai_set_id):
        """Get an OaiSet by its id.

        Args:
            oai_set_id: OaiSet id.

        Returns: The OaiSet instance.

        Raises:
            DoesNotExist: The set doesn't exist
            ModelError: Internal error during the process

        """
        try:
            return OaiProviderSet.objects.get(pk=str(oai_set_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_all(order_by_field=None):
        """Return all OaiProviderSet.
        Args:
            order_by_field: Order by field.
        Returns:
            List of OaiProviderSet.

        """
        if not order_by_field:
            return OaiProviderSet.objects.all()

        return OaiProviderSet.objects.order_by(
            *[field.replace("+", "") for field in order_by_field]
        )

    @staticmethod
    def get_all_by_templates_manager(templates_manager):
        """Get all OaiProviderSet used by a list of templates_manager

        Args:
            templates_manager: List of templates manager

        Returns:
            List of OaiProviderSet.

        """
        return OaiProviderSet.objects.filter(
            templates_manager__in=templates_manager
        ).all()

    @staticmethod
    def get_by_set_spec(set_spec):
        """Get an OaiProviderSet by its set_spec.

        Args:
            set_spec: OaiProviderSet set_spec.

        Returns:
            The OaiProviderSet instance.

        Raises:
            DoesNotExist: The set doesn't exist
            ModelError: Internal error during the process

        """
        try:
            return OaiProviderSet.objects.get(set_spec=set_spec)
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))
