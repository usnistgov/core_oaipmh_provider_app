""" Tests unit
"""

from random import randint
from unittest.case import TestCase

from unittest.mock import Mock, patch

from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
import core_oaipmh_provider_app.components.oai_provider_metadata_format.api as provider_metadata_format_api
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import (
    OaiProviderMetadataFormat,
)


class TestOaiProviderMetadataFormatUpsert(TestCase):
    """Test Oai Provider Metadata Format Upsert"""

    def setUp(self):
        """setUp"""
        self.mock_oai_provider_metadata_format = (
            _create_oai_provider_metadata_format()
        )

    @patch.object(OaiProviderMetadataFormat, "save")
    def test_oai_provider_metadata_format_upsert_returns_object(
        self, mock_save
    ):
        """test_oai_provider_metadata_format_upsert_returns_object"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_save.return_value = self.mock_oai_provider_metadata_format

        # Act
        result = provider_metadata_format_api.upsert(
            self.mock_oai_provider_metadata_format, request=mock_request
        )

        # Assert
        self.assertIsInstance(result, OaiProviderMetadataFormat)

    @patch.object(OaiProviderMetadataFormat, "save")
    def test_oai_provider_metadata_format_upsert_raises_error_if_save_failed(
        self, mock_save
    ):
        """test_oai_provider_metadata_format_upsert_raises_error_if_save_failed"""

        # Arrange
        mock_save.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            provider_metadata_format_api.upsert(
                self.mock_oai_provider_metadata_format
            )


class TestOaiProviderMetadataFormatGetById(TestCase):
    """Test Oai Provider Metadata Format Get By Id"""

    @patch.object(OaiProviderMetadataFormat, "get_by_id")
    def test_get_by_id_return_object(self, mock_get_by_id):
        """test_get_by_id_return_object"""

        # Arrange
        mock_oai_provider_metadata_format = (
            _create_mock_oai_provider_metadata_format()
        )
        mock_oai_provider_metadata_format.id = randint(1, 100)

        mock_get_by_id.return_value = mock_oai_provider_metadata_format

        # Act
        result = provider_metadata_format_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, OaiProviderMetadataFormat)

    @patch.object(OaiProviderMetadataFormat, "get_by_id")
    def test_get_by_id_raises_exception_if_object_does_not_exist(
        self, mock_get_by_id
    ):
        """test_get_by_id_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_id = randint(1, 100)

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            provider_metadata_format_api.get_by_id(mock_absent_id)

    @patch.object(OaiProviderMetadataFormat, "get_by_id")
    def test_get_by_id_raises_exception_if_internal_error(
        self, mock_get_by_id
    ):
        """test_get_by_id_raises_exception_if_internal_error"""

        # Arrange
        mock_absent_id = randint(1, 100)

        mock_get_by_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            provider_metadata_format_api.get_by_id(mock_absent_id)


class TestOaiProviderMetadataFormatGetByMetadataPrefix(TestCase):
    """Test Oai Provider Metadata Format Get By Metadata Prefix"""

    @patch.object(OaiProviderMetadataFormat, "get_by_metadata_prefix")
    def test_get_by_metadata_prefix_return_object(self, mock_get):
        """test_get_by_metadata_prefix_return_object"""

        # Arrange
        mock_oai_provider_metadata_format = (
            _create_mock_oai_provider_metadata_format()
        )

        mock_get.return_value = mock_oai_provider_metadata_format

        # Act
        result = provider_metadata_format_api.get_by_metadata_prefix(
            mock_oai_provider_metadata_format.metadata_prefix
        )

        # Assert
        self.assertIsInstance(result, OaiProviderMetadataFormat)

    @patch.object(OaiProviderMetadataFormat, "get_by_metadata_prefix")
    def test_get_by_metadata_prefix_raises_exception_if_object_does_not_exist(
        self, mock_get
    ):
        """test_get_by_metadata_prefix_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_metadata_prefix = randint(1, 100)

        mock_get.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            provider_metadata_format_api.get_by_metadata_prefix(
                mock_absent_metadata_prefix
            )

    @patch.object(OaiProviderMetadataFormat, "get_by_metadata_prefix")
    def test_get_by_metadata_prefix_raises_exception_if_internal_error(
        self, mock_get
    ):
        """test_get_by_metadata_prefix_raises_exception_if_internal_error"""

        # Arrange
        mock_absent_metadata_prefix = randint(1, 100)

        mock_get.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            provider_metadata_format_api.get_by_metadata_prefix(
                mock_absent_metadata_prefix
            )


class TestOaiProviderMetadataFormatGetAll(TestCase):
    """Test Oai Provider Metadata Format Get All"""

    @patch.object(OaiProviderMetadataFormat, "get_all")
    def test_get_all_contains_only_oai_provider_metadata_format(
        self, mock_get_all
    ):
        """test_get_all_contains_only_oai_provider_metadata_format"""
        _generic_get_all_test(
            self, mock_get_all, provider_metadata_format_api.get_all()
        )


class TestOaiProviderMetadataFormatGetAllCustomMetadataFormat(TestCase):
    """Test Oai Provider Metadata Format Get All Custom Metadata Format"""

    @patch.object(OaiProviderMetadataFormat, "get_all_custom_metadata_format")
    def test_get_all_custom_metadata_format_contains_only_oai_provider_metadata_format(
        self, mock_get_all
    ):
        """test_get_all_custom_metadata_format_contains_only_oai_provider_metadata_format"""

        _generic_get_all_test(
            self,
            mock_get_all,
            provider_metadata_format_api.get_all_custom_metadata_format(),
        )


class TestOaiProviderMetadataFormatGetAllDefaultMetadataFormat(TestCase):
    """Test Oai Provider Metadata Format Get All Default Metadata Format"""

    @patch.object(OaiProviderMetadataFormat, "get_all_default_metadata_format")
    def test_get_all_default_metadata_format_contains_only_oai_provider_metadata_format(
        self, mock_get_all
    ):
        """test_get_all_default_metadata_format_contains_only_oai_provider_metadata_format"""

        _generic_get_all_test(
            self,
            mock_get_all,
            provider_metadata_format_api.get_all_default_metadata_format(),
        )


class TestOaiProviderMetadataFormatGetAllTemplateMetadataFormat(TestCase):
    """Test Oai Provider Metadata Format Get All Template Metadata Format"""

    @patch.object(
        OaiProviderMetadataFormat, "get_all_template_metadata_format"
    )
    def test_get_all_template_metadata_format_contains_only_oai_provider_metadata_format(
        self, mock_get_all
    ):
        """test_get_all_template_metadata_format_contains_only_oai_provider_metadata_format"""

        _generic_get_all_test(
            self,
            mock_get_all,
            provider_metadata_format_api.get_all_template_metadata_format(),
        )


class TestOaiProviderMetadataFormatGetAllNoTemplateMetadataFormat(TestCase):
    """Test Oai Provider Metadata Format Get All No Template Metadata Format"""

    @patch.object(
        OaiProviderMetadataFormat, "get_all_no_template_metadata_format"
    )
    def test_get_all_not_template_metadata_format_contains_only_oai_provider_metadata_format(
        self, mock_get_all
    ):
        """test_get_all_not_template_metadata_format_contains_only_oai_provider_metadata_format"""

        _generic_get_all_test(
            self,
            mock_get_all,
            provider_metadata_format_api.get_all_no_template_metadata_format(),
        )


class TestOaiProviderMetadataFormatGetAllByTemplates(TestCase):
    """Test Oai Provider Metadata Format Get All By Templates"""

    @patch.object(OaiProviderMetadataFormat, "get_all_by_templates")
    def test_get_all_by_templates_return_object(self, mock_get):
        """test_get_all_by_templates_return_object"""

        # Arrange
        mock_oai_provider_metadata_format1 = (
            _create_mock_oai_provider_metadata_format()
        )
        mock_oai_provider_metadata_format2 = (
            _create_mock_oai_provider_metadata_format()
        )

        mock_get.return_value = [
            mock_oai_provider_metadata_format1,
            mock_oai_provider_metadata_format2,
        ]

        # Act
        result = provider_metadata_format_api.get_all_by_templates(
            [
                mock_oai_provider_metadata_format1.template,
                mock_oai_provider_metadata_format2.template,
            ]
        )

        # Assert
        self.assertTrue(
            all(isinstance(item, OaiProviderMetadataFormat) for item in result)
        )


class TestOaiProviderMetadataFormatDelete(TestCase):
    """Test Oai Provider Metadata Format Delete"""

    @patch.object(OaiProviderMetadataFormat, "delete")
    def test_delete_oai_provider_metadata_format_raises_exception_if_error(
        self, mock_delete
    ):
        """test_delete_oai_provider_metadata_format_raises_exception_if_error"""

        # Arrange
        oai_provider_metadata_format = _create_oai_provider_metadata_format()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            provider_metadata_format_api.delete(oai_provider_metadata_format)


class TestOaiProviderMetadataFormatGetMetadataFormatSchemaUrl(TestCase):
    """Test Oai Provider Metadata Format Get Metadata Format Schema Url"""

    def test_get_metadata_format_schema_url_returns(self):
        """test_get_metadata_format_schema_url_returns"""

        # Arrange
        mock_oai_provider_metadata_format1 = (
            _create_mock_oai_provider_metadata_format(is_template=False)
        )

        # Act
        result = provider_metadata_format_api.get_metadata_format_schema_url(
            mock_oai_provider_metadata_format1
        )

        # Assert
        self.assertEqual(mock_oai_provider_metadata_format1.schema, result)


class TestOaiProviderMetadataFormatGetSimpleTemplateMetadataFormatSchemaUrl(
    TestCase
):
    """Test Oai Provider Metadata Format Get Simple Template Metadata Format Schema Url"""

    def test_get_simple_template_metadata_format_schema_url_returns(self):
        """test_get_simple_template_metadata_format_schema_url_returns"""

        # Arrange
        title = "Schema"
        version = 1

        # Act
        result = provider_metadata_format_api._get_simple_template_metadata_format_schema_url(
            title, version
        )

        # Assert
        self.assertEqual("Schema/1", result)


def _generic_get_all_test(self, mock_get_all, act_function):
    # Arrange
    mock_oai_provider_metadata_format1 = (
        _create_mock_oai_provider_metadata_format()
    )
    mock_oai_provider_metadata_format2 = (
        _create_mock_oai_provider_metadata_format()
    )

    mock_get_all.return_value = [
        mock_oai_provider_metadata_format1,
        mock_oai_provider_metadata_format2,
    ]

    # Act
    result = act_function

    # Assert
    self.assertTrue(
        all(isinstance(item, OaiProviderMetadataFormat) for item in result)
    )


def _create_oai_provider_metadata_format():
    """Get an OaiProviderMetadataFormat object.

    Returns:
        OaiProviderMetadataFormat instance.

    """
    oai_provider_metadata_format = OaiProviderMetadataFormat()
    _set_oai_provider_metadata_format_fields(oai_provider_metadata_format)

    return oai_provider_metadata_format


def _create_mock_oai_provider_metadata_format(is_template=False):
    """Mock an OaiProviderMetadataFormat.

    Returns:
        OaiProviderMetadataFormat mock.

    """
    mock_oai_provider_metadata_format = Mock(spec=OaiProviderMetadataFormat)
    _set_oai_provider_metadata_format_fields(
        mock_oai_provider_metadata_format, is_template
    )

    return mock_oai_provider_metadata_format


def _set_oai_provider_metadata_format_fields(
    oai_provider_metadata_format,
    is_template=False,
    schema="http://test.com/test.xsd",
):
    """Set OaiProviderMetadataFormat fields.

    Returns:
        OaiProviderMetadataFormat with assigned fields.

    """
    oai_provider_metadata_format.metadata_prefix = "test"
    oai_provider_metadata_format.schema = schema
    oai_provider_metadata_format.xml_schema = (
        "<schema xmlns='http://www.w3.org/2001/XMLSchema'></schema>"
    )
    oai_provider_metadata_format.metadata_namespace = "http://test.com/meta"
    oai_provider_metadata_format.is_default = True
    oai_provider_metadata_format.is_template = is_template
    oai_provider_metadata_format.template = None

    return oai_provider_metadata_format
