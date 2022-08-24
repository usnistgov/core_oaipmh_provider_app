"""
OaiSettings model
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from core_main_app.commons import exceptions


class OaiSettings(models.Model):
    """Represents the settings for Oai-Pmh Provider"""

    repository_name = models.CharField(max_length=255)
    repository_identifier = models.CharField(max_length=255)
    enable_harvesting = models.BooleanField()

    class Meta:
        verbose_name = "Oai settings"
        verbose_name_plural = "Oai settings"

    @staticmethod
    def get():
        """Get the settings.

        Returns: The OaiSettings instance.

        Raises:
            DoesNotExist: The settings doesn't exist.
            ModelError: Internal error during the process.

        """
        try:
            return OaiSettings.objects.get()
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))
