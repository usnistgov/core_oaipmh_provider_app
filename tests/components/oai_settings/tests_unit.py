""" Tests unit
"""

from unittest.case import TestCase

from unittest.mock import Mock, patch

from core_main_app.commons import exceptions
import core_oaipmh_provider_app.components.oai_settings.api as settings_api
from core_oaipmh_provider_app.components.oai_settings.models import OaiSettings


class TestOaiSettingsGet(TestCase):
    """Test Oai Settings Get"""

    @patch.object(OaiSettings, "get")
    def test_get_return_object(self, mock_get):
        """test_get_return_object"""

        # Arrange
        mock_oai_settings = _create_mock_oai_settings()

        mock_get.return_value = mock_oai_settings

        # Act
        result = settings_api.get()

        # Assert
        self.assertIsInstance(result, OaiSettings)

    @patch.object(OaiSettings, "get")
    def test_get_raises_exception_if_object_does_not_exist(self, mock_get):
        """test_get_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("Error")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            settings_api.get()

    @patch.object(OaiSettings, "get")
    def test_get_raises_exception_if_internal_error(self, mock_get):
        """test_get_raises_exception_if_internal_error"""

        # Arrange
        mock_get.side_effect = exceptions.ModelError("Error")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            settings_api.get()


class TestOaiSettingsUpsert(TestCase):
    """Test Oai Settings Upsert"""

    @patch.object(OaiSettings, "save")
    def test_upsert_oai_settings_raises_exception_if_save_failed(
        self, mock_save
    ):
        """test_upsert_oai_settings_raises_exception_if_save_failed"""

        # Arrange
        oai_settings = _create_oai_settings()

        mock_save.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(Exception):
            settings_api.upsert(oai_settings)


def _create_oai_settings():
    """Get an OaiSettings object.

    Returns:
        OaiSettings instance.

    """
    oai_settings = OaiSettings()
    _set_oai_setting_fields(oai_settings)

    return oai_settings


def _create_mock_oai_settings():
    """Mock an OaiSettings.

    Returns:
        OaiSettings mock.

    """
    mock_oai_settings = Mock(spec=OaiSettings)
    _set_oai_setting_fields(mock_oai_settings)

    return mock_oai_settings


def _set_oai_setting_fields(oai_settings):
    """Set OaiSettings fields.

    Args:
        oai_settings:

    Returns:
        OaiSettings with assigned fields.

    """
    oai_settings.repository_name = "Repository"
    oai_settings.repository_identifier = "identifier"
    oai_settings.enable_harvesting = True

    return oai_settings
