""" OaiRequestPage model
"""
from django_mongoengine import fields, Document
from mongoengine import errors as mongoengine_errors

from core_main_app.commons import exceptions


class OaiRequestPage(Document):
    """Informations about a request sent by a harvester needed a paginated
    response.
    """

    resumption_token = fields.StringField(blank=False, unique=True)
    template_id_list = fields.ListField(blank=False)
    metadata_format = fields.StringField(blank=False)
    oai_set = fields.StringField(blank=True, default=None)
    from_date = fields.DateTimeField(blank=True, default=None)
    until_date = fields.DateTimeField(blank=True, default=None)
    expiration_date = fields.DateTimeField(blank=False, default=None)
    page_number = fields.IntField(blank=False)

    @staticmethod
    def get_by_resumption_token(resumption_token):
        try:
            return OaiRequestPage.objects.get(resumption_token=resumption_token)
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
