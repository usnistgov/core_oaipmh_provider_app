"""
OaiXslTemplate model
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import (
    OaiProviderMetadataFormat,
)


class OaiXslTemplate(models.Model):
    """Relation between a template, an OaiProviderMetadataFormat and a XSLT."""

    template = models.ForeignKey(
        Template, blank=False, on_delete=models.CASCADE
    )
    xslt = models.ForeignKey(
        XslTransformation, blank=False, on_delete=models.CASCADE
    )
    oai_metadata_format = models.ForeignKey(
        OaiProviderMetadataFormat,
        blank=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        """Meta"""

        unique_together = ("oai_metadata_format", "xslt", "template")

    @staticmethod
    def get_by_id(oai_xslt_template_id):
        """Returns the object with the given id

        Args:
            oai_xslt_template_id: Object id.

        Returns:
            OaiXslTemplate (obj): OaiXslTemplate object with the given id.

        Raises:
            DoesNotExist: The OaiXslTemplate doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiXslTemplate.objects.get(pk=str(oai_xslt_template_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))

    @staticmethod
    def get_by_template_id_and_metadata_format_id(
        template_id, metadata_format_id
    ):
        """Returns an OaiXslTemplate by its template and metadata_format.
        Args:
            template_id: Template id.
            metadata_format_id: Metadata format id.

        Returns:
            OaiXslTemplate instance.

        Raises:
            DoesNotExist: The metadata format doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiXslTemplate.objects.get(
                template=template_id, oai_metadata_format=metadata_format_id
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_all_by_templates(templates):
        """Returns all OaiXslTemplate used by a list of templates.

        Args:
            templates: List of templates.

        Returns:
            List of OaiXslTemplate.

        """
        return OaiXslTemplate.objects.filter(template__in=templates).all()

    @staticmethod
    def get_all_by_metadata_format(metadata_format):
        """Returns all OaiXslTemplate used by a metadata format.

        Args:
            metadata_format: OaiProviderMetadataFormat.

        Returns:
            List of OaiXslTemplate.

        """
        return OaiXslTemplate.objects.filter(
            oai_metadata_format=metadata_format
        ).all()

    def save_object(self):
        """Custom save.

        Returns:
            Saved Instance.

        """
        try:
            return self.save()
        except IntegrityError as exception:
            raise exceptions.NotUniqueError(str(exception))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
