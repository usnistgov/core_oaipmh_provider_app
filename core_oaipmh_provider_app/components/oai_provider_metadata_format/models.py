"""
OaiProviderMetadataFormat model
"""

from django_mongoengine import fields
from mongoengine.queryset.base import CASCADE
from core_oaipmh_common_app.components.oai_metadata_format.models import OaiMetadataFormat
from core_main_app.components.template.models import Template


class OaiProviderMetadataFormat(OaiMetadataFormat):
    """Represents a metadata format for Oai-Pmh Provider"""
    isDefault = fields.BooleanField(blank=True)
    isTemplate = fields.BooleanField(blank=True)
    template = fields.ReferenceField(Template, reverse_delete_rule=CASCADE)

    @staticmethod
    def get_all_custom_metadata_format():
        """ Get all custom OaiProviderMetadataFormat.

            Returns:
                List of metadata format.

        """
        return OaiProviderMetadataFormat.objects(isDefault=False, isTemplate=False or None).all()

    @staticmethod
    def get_all_default_metadata_format():
        """ Get all default OaiProviderMetadataFormat.

            Returns:
                List of metadata format.

        """
        return OaiProviderMetadataFormat.objects(isDefault=True).all()

    @staticmethod
    def get_all_template_metadata_format():
        """ Get all OaiProviderMetadataFormat based on a template.

            Returns:
                List of metadata format.

        """
        return OaiProviderMetadataFormat.objects(isTemplate=True).all()

    @staticmethod
    def get_all_no_template_metadata_format():
        """ Get all OaiProviderMetadataFormat except the metadata formats based on a template.

            Returns:
                List of metadata format.

        """
        return OaiProviderMetadataFormat.objects(isTemplate=False or None).all()

    @staticmethod
    def get_all_by_templates(templates):
        """ Get all OaiProviderMetadataFormat used by a list of templates.

            Returns:
                List of metadata format.

        """
        return OaiProviderMetadataFormat.objects(template__in=templates, isTemplate=True).all()
