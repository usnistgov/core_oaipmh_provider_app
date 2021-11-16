""" OaiRequestPage model
"""
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from core_main_app.commons import exceptions


class OaiRequestPage(models.Model):
    """Informations about a request sent by a harvester needed a paginated
    response.
    """

    resumption_token = models.CharField(max_length=255, blank=False, unique=True)
    metadata_format = models.CharField(max_length=255, blank=False)
    template_id_list = models.JSONField(default=[], blank=False)
    oai_set = models.CharField(max_length=255, blank=True, default=None)
    from_date = models.DateTimeField(blank=True, default=None)
    until_date = models.DateTimeField(blank=True, default=None)
    expiration_date = models.DateTimeField(blank=False, default=None)
    page_number = models.IntegerField(blank=False)

    @staticmethod
    def get_by_resumption_token(resumption_token):
        try:
            return OaiRequestPage.objects.get(resumption_token=resumption_token)
        except ObjectDoesNotExist as e:
            raise exceptions.DoesNotExist(str(e))
        except Exception as ex:
            raise exceptions.ModelError(str(ex))
