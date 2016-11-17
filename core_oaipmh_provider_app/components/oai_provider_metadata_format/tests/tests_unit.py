from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
import core_oaipmh_provider_app.components.oai_provider_metadata_format.api as provider_metadata_format_api
from core_main_app.commons import exceptions
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import OaiProviderMetadataFormat


class TestOaiProviderMetadataFormatUpsert(TestCase):
    def setUp(self):
        self.mock_oai_provider_metadata_format = _create_oai_provider_metadata_format()

    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.save')
    def test_oai_provider_metadata_format_upsert_returns_object(self, mock_save):
        # Arrange
        mock_save.return_value = self.mock_oai_provider_metadata_format

        # Act
        result = provider_metadata_format_api.upsert(self.mock_oai_provider_metadata_format)

        # Assert
        self.assertIsInstance(result, OaiProviderMetadataFormat)

    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.save')
    def test_oai_provider_metadata_format_upsert_raises_error_if_save_failed(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            provider_metadata_format_api.upsert(self.mock_oai_provider_metadata_format)


class TestOaiProviderMetadataFormatGetById(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.'
           'get_by_id')
    def test_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        mock_oai_provider_metadata_format = _create_mock_oai_provider_metadata_format()
        mock_oai_provider_metadata_format.id = ObjectId()

        mock_get_by_id.return_value = mock_oai_provider_metadata_format

        # Act
        result = provider_metadata_format_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, OaiProviderMetadataFormat)

    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.'
           'get_by_id')
    def test_get_by_id_raises_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            provider_metadata_format_api.get_by_id(mock_absent_id)


class TestOaiProviderMetadataFormatGetByMetadataPrefix(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.'
           'get_by_metadata_prefix')
    def test_get_by_metadata_prefix_return_object(self, mock_get):
        # Arrange
        mock_oai_provider_metadata_format = _create_mock_oai_provider_metadata_format()

        mock_get.return_value = mock_oai_provider_metadata_format

        # Act
        result = provider_metadata_format_api.get_by_metadata_prefix(mock_oai_provider_metadata_format.metadataPrefix)

        # Assert
        self.assertIsInstance(result, OaiProviderMetadataFormat)

    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.'
           'get_by_metadata_prefix')
    def test_get_by_metadata_prefix_raises_exception_if_object_does_not_exist(self, mock_get):
        # Arrange
        mock_absent_metadata_prefix = ObjectId()

        mock_get.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            provider_metadata_format_api.get_by_metadata_prefix(mock_absent_metadata_prefix)


class TestOaiProviderMetadataFormatGetAll(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.get_all')
    def test_get_all_contains_only_oai_provider_metadata_format(self, mock_get_all):
        _generic_get_all_test(self, mock_get_all, provider_metadata_format_api.get_all())


class TestOaiProviderMetadataFormatGetAllCustomMetadataFormat(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.'
           'get_all_custom_metadata_format')
    def test_get_all_custom_metadata_format_contains_only_oai_provider_metadata_format(self, mock_get_all):
        _generic_get_all_test(self, mock_get_all, provider_metadata_format_api.get_all_custom_metadata_format())


class TestOaiProviderMetadataFormatGetAllDefaultMetadataFormat(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.'
           'get_all_default_metadata_format')
    def test_get_all_default_metadata_format_contains_only_oai_provider_metadata_format(self, mock_get_all):
        _generic_get_all_test(self, mock_get_all, provider_metadata_format_api.get_all_default_metadata_format())


class TestOaiProviderMetadataFormatGetAllTemplateMetadataFormat(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.'
           'get_all_template_metadata_format')
    def test_get_all_template_metadata_format_contains_only_oai_provider_metadata_format(self, mock_get_all):
        _generic_get_all_test(self, mock_get_all, provider_metadata_format_api.get_all_template_metadata_format())


class TestOaiProviderMetadataFormatGetAllNoTemplateMetadataFormat(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.'
           'get_all_no_template_metadata_format')
    def test_get_all_not_template_metadata_format_contains_only_oai_provider_metadata_format(self, mock_get_all):
        _generic_get_all_test(self, mock_get_all, provider_metadata_format_api.get_all_no_template_metadata_format())


class TestOaiProviderMetadataFormatGetAllByTemplates(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.'
           'get_all_by_templates')
    def test_get_all_by_templates_return_object(self, mock_get):
        # Arrange
        mock_oai_provider_metadata_format1 = _create_mock_oai_provider_metadata_format()
        mock_oai_provider_metadata_format2 = _create_mock_oai_provider_metadata_format()

        mock_get.return_value = [mock_oai_provider_metadata_format1, mock_oai_provider_metadata_format2]

        # Act
        result = provider_metadata_format_api.get_all_by_templates([mock_oai_provider_metadata_format1.template,
                                                                    mock_oai_provider_metadata_format2.template])

        # Assert
        self.assertTrue(all(isinstance(item, OaiProviderMetadataFormat) for item in result))


class TestOaiProviderMetadataFormatDelete(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_metadata_format.models.OaiProviderMetadataFormat.delete')
    def test_delete_oai_provider_metadata_format_raises_exception_if_object_does_not_exist(self, mock_delete):
        # Arrange
        oai_provider_metadata_format = _create_oai_provider_metadata_format()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            provider_metadata_format_api.delete(oai_provider_metadata_format)


def _generic_get_all_test(self, mock_get_all, act_function):
    # Arrange
    mock_oai_provider_metadata_format1 = _create_mock_oai_provider_metadata_format()
    mock_oai_provider_metadata_format2 = _create_mock_oai_provider_metadata_format()

    mock_get_all.return_value = [mock_oai_provider_metadata_format1, mock_oai_provider_metadata_format2]

    # Act
    result = act_function

    # Assert
    self.assertTrue(all(isinstance(item, OaiProviderMetadataFormat) for item in result))


def _create_oai_provider_metadata_format():
    """ Get an OaiProviderMetadataFormat object.

        Returns:
            OaiProviderMetadataFormat instance.

    """
    oai_provider_metadata_format = OaiProviderMetadataFormat()
    _set_oai_provider_metadata_format_fields(oai_provider_metadata_format)

    return oai_provider_metadata_format


def _create_mock_oai_provider_metadata_format():
    """ Mock an OaiProviderMetadataFormat.

        Returns:
            OaiProviderMetadataFormat mock.

    """
    mock_oai_provider_metadata_format = Mock(spec=OaiProviderMetadataFormat)
    _set_oai_provider_metadata_format_fields(mock_oai_provider_metadata_format)

    return mock_oai_provider_metadata_format


def _set_oai_provider_metadata_format_fields(oai_provider_metadata_format):
    """ Set OaiProviderMetadataFormat fields.

        Returns:
            OaiProviderMetadataFormat with assigned fields.

    """
    oai_provider_metadata_format.metadataPrefix = "test"
    oai_provider_metadata_format.schema = "http://test.com/test.xsd"
    oai_provider_metadata_format.xmlSchema = "<root><test>Hello</test></root>"
    oai_provider_metadata_format.metadataNamespace = 'http://test.com/meta'
    oai_provider_metadata_format.isDefault = True
    oai_provider_metadata_format.isTemplate = False
    oai_provider_metadata_format.template = None

    return oai_provider_metadata_format
