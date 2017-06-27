"""
    Serializers used throughout the Rest API
"""
from core_main_app.commons.serializers import BasicSerializer
from rest_framework.serializers import CharField, ListField, BooleanField
from rest_framework_mongoengine.serializers import DocumentSerializer
from core_oaipmh_provider_app.components.oai_provider_set.models import OaiProviderSet
from core_oaipmh_provider_app.components.oai_settings.models import OaiSettings
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import OaiProviderMetadataFormat
import core_main_app.components.version_manager.api as version_manager_api


class MetadataFormatIdSerializer(BasicSerializer):
    metadata_format_id = CharField(required=True)


class SetIdSerializer(BasicSerializer):
    set_id = CharField(required=True)


class SettingsSerializer(DocumentSerializer):
    class Meta:
        model = OaiSettings
        fields = "__all__"


class OaiProviderMetadataFormatSerializer(DocumentSerializer):
    class Meta:
        model = OaiProviderMetadataFormat
        fields = "__all__"
        depth = 2


class OaiProviderSetSerializer(DocumentSerializer):
    class Meta:
        model = OaiProviderSet
        # TODO: Add template_manager
        fields = ['id', 'set_spec', 'set_name', 'description']
        depth = 2


class AddMetadataFormatSerializer(BasicSerializer):
    metadata_prefix = CharField(required=True)
    schema = CharField(required=True)


class AddTemplateMetadataFormatSerializer(BasicSerializer):
    metadata_prefix = CharField(required=True)
    template_id = CharField(required=True)


class AddSetSerializer(BasicSerializer):
    def create(self, validated_data):
        return OaiProviderSet(**validated_data)

    set_spec = CharField(required=True)
    set_name = CharField(required=True)
    templates_manager = ListField(child=CharField(), required=True)
    description = CharField(required=True)


class UpdateSettingsSerializer(BasicSerializer):
    def update(self, instance, validated_data):
        instance.repository_name = validated_data.get('repository_name', instance.repository_name)
        instance.repository_identifier = validated_data.get('repository_identifier', instance.repository_identifier)
        instance.enable_harvesting = validated_data.get('enable_harvesting', instance.enable_harvesting)
        return instance

    repository_name = CharField(required=False)
    repository_identifier = CharField(required=False)
    enable_harvesting = BooleanField(required=False)


class UpdateMetadataFormatSerializer(BasicSerializer):
    def update(self, instance, validated_data):
        instance.metadata_prefix = validated_data.get('metadata_prefix')
        return instance

    metadata_format_id = CharField(required=True)
    metadata_prefix = CharField(required=True)


class UpdateSetSerializer(BasicSerializer):
    def update(self, instance, validated_data):
        instance.set_spec = validated_data.get('set_spec', instance.set_spec)
        instance.set_name = validated_data.get('set_name', instance.set_name)
        templates_manager = validated_data.get('templates_manager', None)
        if templates_manager is not None:
            templates_manager = [version_manager_api.get(id_) for id_ in templates_manager]
            instance.templates_manager = templates_manager
        instance.description = validated_data.get('description', instance.description)
        return instance

    set_id = CharField(required=True)
    set_spec = CharField(required=False)
    set_name = CharField(required=False)
    templates_manager = ListField(child=CharField(), required=False)
    description = CharField(required=False)


class TemplateToMFMappingXSLTSerializer(BasicSerializer):
    template_id = CharField(required=True)
    metadata_format_id = CharField(required=True)
    xslt_id = CharField(required=True)


class TemplateToMFUnMappingXSLTSerializer(BasicSerializer):
    template_id = CharField(required=True)
    metadata_format_id = CharField(required=True)
