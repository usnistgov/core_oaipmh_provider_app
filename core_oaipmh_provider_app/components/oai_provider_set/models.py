"""
OaiProviderSet model
"""

from django_mongoengine import fields
from mongoengine.queryset.base import PULL
from core_oaipmh_common_app.components.oai_set.models import OaiSet
from core_main_app.components.template.models import Template


class OaiProviderSet(OaiSet):
    """Represents a set for Oai-Pmh Provider"""
    templates = fields.ListField(fields.ReferenceField(Template, reverse_delete_rule=PULL))
    description = fields.StringField(blank=True)

    def update_object(self):
        """
        Update the OaiProviderSet
        :param:
        :return:
        """
        self.update()

    @staticmethod
    # TODO raise NotUniqueError
    def create_oai_provider_set(set_spec, set_name, templates, description):
        """
        Create a new OaiProviderSet
        :param set_spec:
        :param set_name:
        :param templates:
        :param description:
        :return:
        """
        new_oai_provider_set = OaiProviderSet(setSpec=set_spec,
                                              setName=set_name,
                                              templates=templates,
                                              description=description).save()
        return new_oai_provider_set

    @staticmethod
    def get_all_by_templates(templates):
        """
        Get all OaiProviderSet used by a list of templates
        :param templates:
        :return:
        """
        return OaiProviderSet.objects(templates__in=templates).all()
