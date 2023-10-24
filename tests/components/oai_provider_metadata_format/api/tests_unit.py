""" Unit tests for `core_oaipmh_provider_app.components.oai_provider_metadata_format.api`
package.
"""

from random import randint
from unittest.case import TestCase
from unittest.mock import Mock, patch, MagicMock

from rest_framework import status

import core_oaipmh_provider_app.components.oai_provider_metadata_format.api as provider_metadata_format_api
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_oaipmh_common_app.commons.exceptions import OAIAPILabelledException
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
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        mock_save.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            provider_metadata_format_api.upsert(
                self.mock_oai_provider_metadata_format, request=mock_request
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


class TestAddTemplateMetadataFormat(TestCase):
    """Unit tests for `add_template_metadata_format` function."""

    # FIXME exception throwing has not been tested for this function.

    def setUp(self):
        """setUp"""
        self.user = create_mock_user("1")
        self.mock_request = create_mock_request(self.user)
        self.mock_kwargs = {
            "metadata_prefix": MagicMock(),
            "template_id": MagicMock(),
            "request": self.mock_request,
        }

    @patch.object(provider_metadata_format_api, "Response")
    @patch.object(provider_metadata_format_api, "OaiPmhMessage")
    @patch.object(provider_metadata_format_api, "upsert")
    @patch.object(provider_metadata_format_api, "_get_target_namespace")
    @patch.object(
        provider_metadata_format_api,
        "_get_simple_template_metadata_format_schema_url",
    )
    @patch.object(provider_metadata_format_api, "OaiProviderMetadataFormat")
    @patch.object(provider_metadata_format_api, "version_manager_api")
    @patch.object(provider_metadata_format_api, "template_api")
    def test_get_by_id_called(
        self,
        mock_template_api,
        mock_version_manager_api,
        mock_oai_provider_metadata_format,
        mock_get_simple_template_metadata_format_schema_url,
        mock_get_target_namespace,
        mock_upsert,
        mock_oai_pmh_message,
        mock_response,
    ):
        """test_get_by_id_called"""
        mock_template = MagicMock()
        mock_template.format = Template.XSD
        mock_template_api.get_by_id.return_value = mock_template

        provider_metadata_format_api.add_template_metadata_format(
            **self.mock_kwargs
        )

        mock_template_api.get_by_id.assert_called_with(
            self.mock_kwargs["template_id"], request=self.mock_request
        )

    @patch.object(provider_metadata_format_api, "Response")
    @patch.object(provider_metadata_format_api, "OaiPmhMessage")
    @patch.object(provider_metadata_format_api, "upsert")
    @patch.object(provider_metadata_format_api, "_get_target_namespace")
    @patch.object(
        provider_metadata_format_api,
        "_get_simple_template_metadata_format_schema_url",
    )
    @patch.object(provider_metadata_format_api, "OaiProviderMetadataFormat")
    @patch.object(provider_metadata_format_api, "version_manager_api")
    @patch.object(provider_metadata_format_api, "template_api")
    def test_template_not_xsd_format_raises_oai_exception(
        self,
        mock_template_api,
        mock_version_manager_api,
        mock_oai_provider_metadata_format,
        mock_get_simple_template_metadata_format_schema_url,
        mock_get_target_namespace,
        mock_upsert,
        mock_oai_pmh_message,
        mock_response,
    ):
        """test_template_not_xsd_format_raises_oai_exception"""
        mock_template = MagicMock()
        mock_template.format = Template.JSON
        mock_template_api.get_by_id.return_value = mock_template

        with self.assertRaises(OAIAPILabelledException):
            provider_metadata_format_api.add_template_metadata_format(
                **self.mock_kwargs
            )

    @patch.object(provider_metadata_format_api, "Response")
    @patch.object(provider_metadata_format_api, "OaiPmhMessage")
    @patch.object(provider_metadata_format_api, "upsert")
    @patch.object(provider_metadata_format_api, "_get_target_namespace")
    @patch.object(
        provider_metadata_format_api,
        "_get_simple_template_metadata_format_schema_url",
    )
    @patch.object(provider_metadata_format_api, "OaiProviderMetadataFormat")
    @patch.object(provider_metadata_format_api, "version_manager_api")
    @patch.object(provider_metadata_format_api, "template_api")
    def test_get_version_number_called(
        self,
        mock_template_api,
        mock_version_manager_api,
        mock_oai_provider_metadata_format,
        mock_get_simple_template_metadata_format_schema_url,
        mock_get_target_namespace,
        mock_upsert,
        mock_oai_pmh_message,
        mock_response,
    ):
        """test_get_version_number_called"""
        mock_template = MagicMock()
        mock_template.format = Template.XSD
        mock_template_api.get_by_id.return_value = mock_template

        provider_metadata_format_api.add_template_metadata_format(
            **self.mock_kwargs
        )

        mock_version_manager_api.get_version_number.assert_called_with(
            mock_template.version_manager,
            self.mock_kwargs["template_id"],
            request=self.mock_request,
        )

    @patch.object(provider_metadata_format_api, "Response")
    @patch.object(provider_metadata_format_api, "OaiPmhMessage")
    @patch.object(provider_metadata_format_api, "upsert")
    @patch.object(provider_metadata_format_api, "_get_target_namespace")
    @patch.object(
        provider_metadata_format_api,
        "_get_simple_template_metadata_format_schema_url",
    )
    @patch.object(provider_metadata_format_api, "OaiProviderMetadataFormat")
    @patch.object(provider_metadata_format_api, "version_manager_api")
    @patch.object(provider_metadata_format_api, "template_api")
    def test_get_simple_template_metadata_format_schema_url_called(
        self,
        mock_template_api,
        mock_version_manager_api,
        mock_oai_provider_metadata_format,
        mock_get_simple_template_metadata_format_schema_url,
        mock_get_target_namespace,
        mock_upsert,
        mock_oai_pmh_message,
        mock_response,
    ):
        """test_get_simple_template_metadata_format_schema_url_called"""
        mock_template = MagicMock()
        mock_template.format = Template.XSD
        mock_template_api.get_by_id.return_value = mock_template

        mock_version_number = MagicMock()
        mock_version_manager_api.get_version_number.return_value = (
            mock_version_number
        )

        provider_metadata_format_api.add_template_metadata_format(
            **self.mock_kwargs
        )

        mock_get_simple_template_metadata_format_schema_url.assert_called_with(
            mock_template.version_manager.title, mock_version_number
        )

    @patch.object(provider_metadata_format_api, "Response")
    @patch.object(provider_metadata_format_api, "OaiPmhMessage")
    @patch.object(provider_metadata_format_api, "upsert")
    @patch.object(provider_metadata_format_api, "_get_target_namespace")
    @patch.object(
        provider_metadata_format_api,
        "_get_simple_template_metadata_format_schema_url",
    )
    @patch.object(provider_metadata_format_api, "OaiProviderMetadataFormat")
    @patch.object(provider_metadata_format_api, "version_manager_api")
    @patch.object(provider_metadata_format_api, "template_api")
    def test_get_target_namespace_called(
        self,
        mock_template_api,
        mock_version_manager_api,
        mock_oai_provider_metadata_format,
        mock_get_simple_template_metadata_format_schema_url,
        mock_get_target_namespace,
        mock_upsert,
        mock_oai_pmh_message,
        mock_response,
    ):
        """test_get_target_namespace_called"""
        mock_template = MagicMock()
        mock_template.format = Template.XSD
        mock_template_api.get_by_id.return_value = mock_template

        provider_metadata_format_api.add_template_metadata_format(
            **self.mock_kwargs
        )

        mock_get_target_namespace.assert_called_with(mock_template.content)

    @patch.object(provider_metadata_format_api, "Response")
    @patch.object(provider_metadata_format_api, "OaiPmhMessage")
    @patch.object(provider_metadata_format_api, "upsert")
    @patch.object(provider_metadata_format_api, "_get_target_namespace")
    @patch.object(
        provider_metadata_format_api,
        "_get_simple_template_metadata_format_schema_url",
    )
    @patch.object(provider_metadata_format_api, "OaiProviderMetadataFormat")
    @patch.object(provider_metadata_format_api, "version_manager_api")
    @patch.object(provider_metadata_format_api, "template_api")
    def test_oai_provider_metadata_format_created(
        self,
        mock_template_api,
        mock_version_manager_api,
        mock_oai_provider_metadata_format,
        mock_get_simple_template_metadata_format_schema_url,
        mock_get_target_namespace,
        mock_upsert,
        mock_oai_pmh_message,
        mock_response,
    ):
        """test_oai_provider_metadata_format_created"""
        mock_template = MagicMock()
        mock_template.format = Template.XSD
        mock_template_api.get_by_id.return_value = mock_template

        mock_get_simple_template_metadata_format_schema_url_return_value = (
            MagicMock()
        )
        mock_get_simple_template_metadata_format_schema_url.return_value = (
            mock_get_simple_template_metadata_format_schema_url_return_value
        )

        mock_get_target_namespace_return_value = MagicMock()
        mock_get_target_namespace.return_value = (
            mock_get_target_namespace_return_value
        )

        provider_metadata_format_api.add_template_metadata_format(
            **self.mock_kwargs
        )

        mock_oai_provider_metadata_format.assert_called_with(
            metadata_prefix=self.mock_kwargs["metadata_prefix"],
            schema=mock_get_simple_template_metadata_format_schema_url_return_value,
            xml_schema=mock_template.content,
            is_default=False,
            is_template=True,
            metadata_namespace=mock_get_target_namespace_return_value,
            template=mock_template,
        )

    @patch.object(provider_metadata_format_api, "Response")
    @patch.object(provider_metadata_format_api, "OaiPmhMessage")
    @patch.object(provider_metadata_format_api, "upsert")
    @patch.object(provider_metadata_format_api, "_get_target_namespace")
    @patch.object(
        provider_metadata_format_api,
        "_get_simple_template_metadata_format_schema_url",
    )
    @patch.object(provider_metadata_format_api, "OaiProviderMetadataFormat")
    @patch.object(provider_metadata_format_api, "version_manager_api")
    @patch.object(provider_metadata_format_api, "template_api")
    def test_upsert_called(
        self,
        mock_template_api,
        mock_version_manager_api,
        mock_oai_provider_metadata_format,
        mock_get_simple_template_metadata_format_schema_url,
        mock_get_target_namespace,
        mock_upsert,
        mock_oai_pmh_message,
        mock_response,
    ):
        """test_upsert_called"""
        mock_template = MagicMock()
        mock_template.format = Template.XSD
        mock_template_api.get_by_id.return_value = mock_template

        mock_oai_provider_metadata_format_object = MagicMock()
        mock_oai_provider_metadata_format.return_value = (
            mock_oai_provider_metadata_format_object
        )

        provider_metadata_format_api.add_template_metadata_format(
            **self.mock_kwargs
        )

        mock_upsert.assert_called_with(
            mock_oai_provider_metadata_format_object, request=self.mock_request
        )

    @patch.object(provider_metadata_format_api, "Response")
    @patch.object(provider_metadata_format_api, "OaiPmhMessage")
    @patch.object(provider_metadata_format_api, "upsert")
    @patch.object(provider_metadata_format_api, "_get_target_namespace")
    @patch.object(
        provider_metadata_format_api,
        "_get_simple_template_metadata_format_schema_url",
    )
    @patch.object(provider_metadata_format_api, "OaiProviderMetadataFormat")
    @patch.object(provider_metadata_format_api, "version_manager_api")
    @patch.object(provider_metadata_format_api, "template_api")
    def test_get_message_labelled_called(
        self,
        mock_template_api,
        mock_version_manager_api,
        mock_oai_provider_metadata_format,
        mock_get_simple_template_metadata_format_schema_url,
        mock_get_target_namespace,
        mock_upsert,
        mock_oai_pmh_message,
        mock_response,
    ):
        """test_get_message_labelled_called"""
        mock_template = MagicMock()
        mock_template.format = Template.XSD
        mock_template_api.get_by_id.return_value = mock_template

        provider_metadata_format_api.add_template_metadata_format(
            **self.mock_kwargs
        )

        mock_oai_pmh_message.get_message_labelled.assert_called()

    @patch.object(provider_metadata_format_api, "Response")
    @patch.object(provider_metadata_format_api, "OaiPmhMessage")
    @patch.object(provider_metadata_format_api, "upsert")
    @patch.object(provider_metadata_format_api, "_get_target_namespace")
    @patch.object(
        provider_metadata_format_api,
        "_get_simple_template_metadata_format_schema_url",
    )
    @patch.object(provider_metadata_format_api, "OaiProviderMetadataFormat")
    @patch.object(provider_metadata_format_api, "version_manager_api")
    @patch.object(provider_metadata_format_api, "template_api")
    def test_successful_execution_returns_response_object(
        self,
        mock_template_api,
        mock_version_manager_api,
        mock_oai_provider_metadata_format,
        mock_get_simple_template_metadata_format_schema_url,
        mock_get_target_namespace,
        mock_upsert,
        mock_oai_pmh_message,
        mock_response,
    ):
        """test_successful_execution_returns_response_object"""
        mock_template = MagicMock()
        mock_template.format = Template.XSD
        mock_template_api.get_by_id.return_value = mock_template

        mock_content = MagicMock()
        mock_oai_pmh_message.get_message_labelled.return_value = mock_content

        provider_metadata_format_api.add_template_metadata_format(
            **self.mock_kwargs
        )

        mock_response.assert_called_with(
            mock_content, status=status.HTTP_201_CREATED
        )


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
