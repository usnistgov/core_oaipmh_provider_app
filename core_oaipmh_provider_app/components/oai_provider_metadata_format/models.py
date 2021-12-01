"""
OaiProviderMetadataFormat model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError

from core_main_app.commons import exceptions as exceptions
from core_main_app.components.template.models import Template
from core_oaipmh_common_app.components.oai_metadata_format.models import (
    OaiMetadataFormat,
)


class OaiProviderMetadataFormat(OaiMetadataFormat):
    """Represents a metadata format for Oai-Pmh Provider"""

    is_default = models.BooleanField(blank=True)
    is_template = models.BooleanField(blank=True)
    template = models.ForeignKey(
        Template, on_delete=models.CASCADE, blank=True, null=True
    )

    @staticmethod
    def get_by_id(oai_provider_metadata_format_id):
        try:
            return OaiProviderMetadataFormat.objects.get(
                pk=oai_provider_metadata_format_id
            )
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    @staticmethod
    def get_all():
        """Return all OaiProviderMetadataFormat.

        Returns:
            List of OaiProviderMetadataFormat.

        """
        return OaiProviderMetadataFormat.objects.all()

    @staticmethod
    def get_all_custom_metadata_format(order_by_field=None):
        """Get all custom OaiProviderMetadataFormat.

        Args:
        order_by_field: Order by field.

        Returns:
            List of metadata format.

        """
        return OaiProviderMetadataFormat.objects.filter(
            is_default=False, is_template=False
        ).order_by(order_by_field)

    @staticmethod
    def get_all_default_metadata_format(order_by_field=None):
        """Get all default OaiProviderMetadataFormat.

        Args:
        order_by_field: Order by field.

        Returns:
            List of metadata format.

        """
        return OaiProviderMetadataFormat.objects.filter(is_default=True).order_by(
            order_by_field
        )

    @staticmethod
    def get_all_template_metadata_format(order_by_field=None):
        """Get all OaiProviderMetadataFormat based on a template.

        Args:
        order_by_field: Order by field.

        Returns:
            List of metadata format.

        """
        return OaiProviderMetadataFormat.objects.filter(is_template=True).order_by(
            order_by_field
        )

    @staticmethod
    def get_all_no_template_metadata_format():
        """Get all OaiProviderMetadataFormat except the metadata formats based on a template.

        Returns:
            List of metadata format.

        """
        return OaiProviderMetadataFormat.objects.filter(is_template=False or None).all()

    @staticmethod
    def get_all_by_templates(templates):
        """Get all OaiProviderMetadataFormat used by a list of templates.

        Args:
            The list of templates.

        Returns:
            List of metadata format.

        """
        return OaiProviderMetadataFormat.objects.filter(
            template__in=templates, is_template=True
        ).all()

    @staticmethod
    def get_by_metadata_prefix(metadata_prefix):
        """Get an OaiProviderMetadataFormat by its metadata prefix.

        Args:
            metadata_prefix: OaiProviderMetadataFormat metadata prefix.

        Returns: The OaiProviderMetadataFormat instance.

        Raises:
            DoesNotExist: The metadata format doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiProviderMetadataFormat.objects.get(
                metadata_prefix=metadata_prefix
            )
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as e:
            raise exceptions.ModelError(str(e))

    def __str__(self):
        """String representation of an object.

        Returns:
            String representation

        """
        return self.metadata_prefix
