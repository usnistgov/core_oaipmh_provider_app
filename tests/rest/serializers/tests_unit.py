""" Unit tests for `core_oaipmh_provider_app.rest.serializers` package.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from rest_framework.exceptions import ValidationError

from core_main_app.commons.exceptions import CoreError
from core_oaipmh_provider_app.rest import serializers as rest_serializers


class TestOaiProviderSetListSerializerCreate(TestCase):
    """Unit tests for `OaiProviderSetListSerializer.create` method."""

    def setUp(self):
        """setUp"""
        self.mock_serializer = (
            rest_serializers.OaiProviderSetCreateUpdateSerializer()
        )
        self.mock_serializer._context = {"request": MagicMock()}
        self.mock_kwargs = {"validated_data": MagicMock()}

    @patch.object(rest_serializers, "oai_provider_set_api")
    @patch.object(rest_serializers, "check_template_manager_in_xsd_format")
    def test_check_template_manager_in_xsd_format_core_error_raises_validation_error(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_oai_provider_set_api,
    ):
        """test_check_template_manager_in_xsd_format_core_error_raises_validation_error"""
        mock_check_template_manager_in_xsd_format.side_effect = CoreError(
            "mock_check_template_manager_in_xsd_format_exception"
        )

        with self.assertRaises(ValidationError):
            self.mock_serializer.create(**self.mock_kwargs)

    @patch.object(rest_serializers, "oai_provider_set_api")
    @patch.object(rest_serializers, "check_template_manager_in_xsd_format")
    def test_succesful_execution_returns_set(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_oai_provider_set_api,
    ):
        """test_succesful_execution_returns_set"""
        mock_oai_provider_set = MagicMock()
        mock_oai_provider_set_api.upsert.return_value = mock_oai_provider_set

        self.assertEqual(
            self.mock_serializer.create(**self.mock_kwargs),
            mock_oai_provider_set,
        )


class TestOaiProviderSetListSerializerUpdate(TestCase):
    """Unit tests for `OaiProviderSetListSerializer.update` method."""

    def setUp(self):
        """setUp"""
        self.mock_serializer = (
            rest_serializers.OaiProviderSetCreateUpdateSerializer()
        )
        self.mock_serializer._context = {"request": MagicMock()}
        self.mock_kwargs = {
            "instance": MagicMock(),
            "validated_data": MagicMock(),
        }

    @patch.object(rest_serializers, "oai_provider_set_api")
    @patch.object(rest_serializers, "template_version_manager_api")
    @patch.object(rest_serializers, "check_template_manager_in_xsd_format")
    def test_check_template_manager_in_xsd_format_core_error_raises_validation_error(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_template_version_manager_api,
        mock_oai_provider_set_api,
    ):
        """test_check_template_manager_in_xsd_format_core_error_raises_validation_error"""
        mock_check_template_manager_in_xsd_format.side_effect = CoreError(
            "mock_check_template_manager_in_xsd_format_exception"
        )

        with self.assertRaises(ValidationError):
            self.mock_serializer.update(**self.mock_kwargs)

    @patch.object(rest_serializers, "oai_provider_set_api")
    @patch.object(rest_serializers, "template_version_manager_api")
    @patch.object(rest_serializers, "check_template_manager_in_xsd_format")
    def test_succesful_execution_returns_set(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_template_version_manager_api,
        mock_oai_provider_set_api,
    ):
        """test_succesful_execution_returns_set"""
        mock_oai_provider_set = MagicMock()
        mock_oai_provider_set_api.upsert.return_value = mock_oai_provider_set

        self.assertEqual(
            self.mock_serializer.update(**self.mock_kwargs),
            mock_oai_provider_set,
        )
