"""Serializers used throughout the Rest API
"""

import logging

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField, ModelSerializer

import core_main_app.components.template_version_manager.api as template_version_manager_api
from core_main_app.commons import exceptions
from core_main_app.commons.serializers import BasicSerializer
from core_main_app.components.xsl_transformation import api as oai_xslt_api
from core_oaipmh_provider_app.components.oai_provider_metadata_format import (
    api as oai_provider_metadata_format_api,
)
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import (
    OaiProviderMetadataFormat,
)
from core_oaipmh_provider_app.components.oai_provider_set import (
    api as oai_provider_set_api,
)
from core_oaipmh_provider_app.components.oai_provider_set.models import OaiProviderSet
from core_oaipmh_provider_app.components.oai_settings import api as oai_settings_api
from core_oaipmh_provider_app.components.oai_settings.models import OaiSettings
from core_oaipmh_provider_app.components.oai_xsl_template import (
    api as oai_xsl_template_api,
)
from core_oaipmh_provider_app.components.oai_xsl_template.models import OaiXslTemplate

logger = logging.getLogger(__name__)


class TemplateMetadataFormatSerializer(BasicSerializer):
    """Template Metadata Format Serializer"""

    metadata_prefix = CharField(required=True)
    template_id = CharField(required=True)

    def create(self, validated_data):
        """create

        Args:
            validated_data:

        Returns:

        """
        return oai_provider_metadata_format_api.add_template_metadata_format(
            **validated_data, request=self.context["request"]
        )


class OaiProviderMetadataFormatSerializer(ModelSerializer):
    """Oai Provider Metadata Format Serializer"""

    schema_url = CharField(required=True, write_only=True)

    class Meta:
        """Meta"""

        model = OaiProviderMetadataFormat
        fields = "__all__"
        depth = 1

        read_only_fields = (
            "id",
            "is_default",
            "is_template",
            "template",
            "schema",
            "xml_schema",
            "metadata_namespace",
        )

    def create(self, validated_data):
        """create

        Args:
            validated_data:

        Returns:

        """
        return oai_provider_metadata_format_api.add_metadata_format(
            **validated_data, request=self.context["request"]
        )


class UpdateMetadataFormatSerializer(BasicSerializer):
    """Update Metadata Format Serializer"""

    def update(self, instance, validated_data):
        """create

        Args:
            instance:
            validated_data:

        Returns:

        """
        instance.metadata_prefix = validated_data.get("metadata_prefix")
        oai_provider_metadata_format_api.upsert(
            instance, request=self.context["request"]
        )

        return instance

    metadata_prefix = CharField(required=True)


class OaiProviderSetSerializer(ModelSerializer):
    """Oai Provider Set Serializer"""

    class Meta:
        """Meta"""

        model = OaiProviderSet
        fields = [
            "id",
            "set_spec",
            "set_name",
            "description",
            "templates_manager",
        ]
        depth = 1

        read_only_fields = ("id",)

    def create(self, validated_data):
        """create

        Args:
            validated_data:

        Returns:

        """
        templates_manager = validated_data.get("templates_manager", [])

        if "templates_manager" in validated_data.keys():
            del validated_data["templates_manager"]

        oai_provider_set = oai_provider_set_api.upsert(OaiProviderSet(**validated_data))
        oai_provider_set.templates_manager.set(templates_manager)

        return oai_provider_set

    def update(self, instance, validated_data):
        """update

        Args:
            instance:
            validated_data:

        Returns:

        """
        instance.set_spec = validated_data.get("set_spec", instance.set_spec)
        instance.set_name = validated_data.get("set_name", instance.set_name)
        templates_manager = validated_data.get("templates_manager", [])
        if len(templates_manager) > 0:
            templates_manager = [
                template_version_manager_api.get_by_id(
                    id_, request=self.context["request"]
                )
                for id_ in templates_manager
            ]
            instance.templates_manager.set(templates_manager)
        instance.description = validated_data.get("description", instance.description)
        return oai_provider_set_api.upsert(instance)


class TemplateToMFMappingXSLTSerializer(ModelSerializer):
    """Template To MF Mapping XSLT Serializer"""

    class Meta:
        """Meta"""

        model = OaiXslTemplate
        fields = "__all__"

    @staticmethod
    def validate_oai_metadata_format(oai_metadata_format):
        """Validate oai_metadata_format field

        Args:
            oai_metadata_format:

        Returns:

        """
        oai_metadata_format_object = oai_provider_metadata_format_api.get_by_id(
            oai_metadata_format
        )

        if oai_metadata_format_object.is_template:
            raise ValidationError(
                "Impossible to map a XSLT to a template metadata format"
            )

        return oai_metadata_format

    def create(self, validated_data):
        """create

        Args:
            validated_data:

        Returns:

        """

        return oai_xsl_template_api.upsert(OaiXslTemplate(**validated_data))

    def update(self, instance, validated_data):
        """update

        Args:
            instance:
            validated_data:

        Returns:

        """
        instance.xslt = oai_xslt_api.get_by_id(validated_data["xslt"])
        return oai_xsl_template_api.upsert(instance)

    def init_instance(self):
        """init_instance

        Returns:

        """

        try:
            oai_xsl_template = (
                oai_xsl_template_api.get_by_template_id_and_metadata_format_id(
                    self.validated_data.get("template", ""),
                    self.validated_data.get("oai_metadata_format", ""),
                )
            )
            self.instance = oai_xsl_template
        except exceptions.DoesNotExist as exception:
            logger.warning("init_instance threw an exception: %s ", str(exception))

    template = CharField(required=True)
    oai_metadata_format = CharField(required=True)
    xslt = CharField(required=True)


class TemplateToMFUnMappingXSLTSerializer(BasicSerializer):
    """Template To MF UnMapping XSLT Serializer"""

    template_id = CharField(required=True)
    metadata_format_id = CharField(required=True)


class SettingsSerializer(ModelSerializer):
    """Settings Serializer"""

    class Meta:
        """Meta"""

        model = OaiSettings
        fields = "__all__"

    def update(self, instance, validated_data):
        """update

        Args:
            instance:
            validated_data:

        Returns:

        """
        instance.repository_name = validated_data.get(
            "repository_name", instance.repository_name
        )
        instance.repository_identifier = validated_data.get(
            "repository_identifier", instance.repository_identifier
        )
        instance.enable_harvesting = validated_data.get(
            "enable_harvesting", instance.enable_harvesting
        )
        return oai_settings_api.upsert(instance)
