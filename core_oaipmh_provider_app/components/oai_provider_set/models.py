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

    @staticmethod
    def get_all_by_templates(templates):
        """
        Get all OaiProviderSet used by a list of templates
        :param templates:
        :return:
        """
        return OaiProviderSet.objects(templates__in=templates).all()
