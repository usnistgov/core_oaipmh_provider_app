""" Test forms from `views.admin.forms`.
"""
from unittest.case import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.utils.tests_tools.RequestMock import create_mock_request

from core_main_app.utils.tests_tools.MockUser import create_mock_user

from core_oaipmh_provider_app.views.admin import forms as admin_forms
from django.test import override_settings


class TestTemplateMetadataFormatForm(TestCase):
    """Test Template Metadata Format Form"""

    @override_settings(BOOTSTRAP_VERSION="4.6.2")
    def test_template_metadata_format_form_bootstrap_v4(self):
        """test_template_metadata_format_form_bootstrap_v4

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=create_mock_user("1"))
        data = {"metadata_prefix": "test"}

        # Act
        form = admin_forms.TemplateMetadataFormatForm(
            data, request=mock_request
        )

        # Assert
        self.assertEqual(
            form.fields["template"].widget.attrs["class"], "form-control"
        )

    @override_settings(BOOTSTRAP_VERSION="5.1.3")
    def test_template_metadata_format_form_bootstrap_v5(self):
        """test_template_metadata_format_form_bootstrap_v5

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=create_mock_user("1"))
        data = {"metadata_prefix": "test"}

        # Act
        form = admin_forms.TemplateMetadataFormatForm(
            data, request=mock_request
        )

        # Assert
        self.assertEqual(
            form.fields["template"].widget.attrs["class"], "form-select"
        )


class TestMappingXSLTForm(TestCase):
    """Test Mapping XSLT Form"""

    @override_settings(BOOTSTRAP_VERSION="4.6.2")
    def test_mapping_xslt_form_bootstrap_v4(self):
        """test_mapping_xslt_form_bootstrap_v4

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=create_mock_user("1"))
        data = {"oai_metadata_format": "test"}

        # Act
        form = admin_forms.MappingXSLTForm(data, request=mock_request)

        # Assert
        self.assertEqual(
            form.fields["template"].widget.attrs["class"], "form-control"
        )
        self.assertEqual(
            form.fields["xslt"].widget.attrs["class"], "form-control"
        )

    @override_settings(BOOTSTRAP_VERSION="5.1.3")
    def test_mapping_xslt_form_bootstrap_v5(self):
        """test_mapping_xslt_form_bootstrap_v5

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=create_mock_user("1"))
        data = {"oai_metadata_format": "test"}

        # Act
        form = admin_forms.MappingXSLTForm(data, request=mock_request)

        # Assert
        self.assertEqual(
            form.fields["template"].widget.attrs["class"], "form-select"
        )
        self.assertEqual(
            form.fields["xslt"].widget.attrs["class"], "form-select"
        )


class TestGetTemplatesVersions(TestCase):
    """Unit tests from `_get_templates_versions` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"request": MagicMock()}

    @patch.object(admin_forms, "template_api")
    @patch.object(admin_forms, "template_version_manager_api")
    def test_get_active_global_version_manager_called(
        self, mock_template_version_manager_api, mock_template_api
    ):
        """test_get_active_global_version_manager_called"""
        admin_forms._get_templates_versions(**self.mock_kwargs)

        mock_template_version_manager_api.get_active_global_version_manager.assert_called_with(
            request=self.mock_kwargs["request"]
        )

    @patch.object(admin_forms, "logger")
    @patch.object(admin_forms, "template_api")
    @patch.object(admin_forms, "template_version_manager_api")
    def test_get_active_global_version_manager_does_not_exist_is_logged(
        self, mock_template_version_manager_api, mock_template_api, mock_logger
    ):
        """test_get_active_global_version_manager_does_not_exist_is_logged"""
        mock_template_version_manager_api.get_active_global_version_manager.side_effect = DoesNotExist(
            "mock_template_version_manager_api_does_not_exist"
        )

        admin_forms._get_templates_versions(**self.mock_kwargs)

        mock_logger.warning.assert_called()

    @patch.object(admin_forms, "logger")
    @patch.object(admin_forms, "template_api")
    @patch.object(admin_forms, "template_version_manager_api")
    def test_get_active_global_version_manager_does_not_exist_returns_empty_list(
        self, mock_template_version_manager_api, mock_template_api, mock_logger
    ):
        """test_get_active_global_version_manager_does_not_exist_returns_empty_list"""
        mock_template_version_manager_api.get_active_global_version_manager.side_effect = DoesNotExist(
            "mock_template_version_manager_api_does_not_exist"
        )

        self.assertEqual(
            admin_forms._get_templates_versions(**self.mock_kwargs), []
        )

    @patch.object(admin_forms, "template_api")
    @patch.object(admin_forms, "template_version_manager_api")
    def test_get_by_id_called(
        self, mock_template_version_manager_api, mock_template_api
    ):
        """test_get_by_id_called"""
        mock_template_version_manager = MagicMock()
        mock_template_version_manager_version = MagicMock()
        mock_template_version_manager.versions = [
            mock_template_version_manager_version
        ]
        mock_template_version_manager_list = [mock_template_version_manager]
        mock_get_active_global_version_manager = MagicMock()
        mock_get_active_global_version_manager.filter.return_value = (
            mock_template_version_manager_list
        )
        mock_template_version_manager_api.get_active_global_version_manager.return_value = (
            mock_get_active_global_version_manager
        )

        admin_forms._get_templates_versions(**self.mock_kwargs)

        mock_template_api.get_by_id.assert_called_with(
            mock_template_version_manager_version,
            request=self.mock_kwargs["request"],
        )

    @patch.object(admin_forms, "logger")
    @patch.object(admin_forms, "template_api")
    @patch.object(admin_forms, "template_version_manager_api")
    def test_get_by_id_does_not_exist_is_logged(
        self, mock_template_version_manager_api, mock_template_api, mock_logger
    ):
        """test_get_by_id_does_not_exist_is_logged"""
        mock_template_version_manager = MagicMock()
        mock_template_version_manager_version = MagicMock()
        mock_template_version_manager.versions = [
            mock_template_version_manager_version
        ]
        mock_template_version_manager_list = [mock_template_version_manager]
        mock_get_active_global_version_manager = MagicMock()
        mock_get_active_global_version_manager.filter.return_value = (
            mock_template_version_manager_list
        )
        mock_template_version_manager_api.get_active_global_version_manager.return_value = (
            mock_get_active_global_version_manager
        )

        mock_template_api.get_by_id.side_effect = DoesNotExist(
            "mock_template_api_get_by_id_does_not_exist"
        )

        admin_forms._get_templates_versions(**self.mock_kwargs)

        mock_logger.warning.assert_called()

    @patch.object(admin_forms, "logger")
    @patch.object(admin_forms, "template_api")
    @patch.object(admin_forms, "template_version_manager_api")
    def test_get_by_id_does_not_exist_returns_empty_list(
        self, mock_template_version_manager_api, mock_template_api, mock_logger
    ):
        """test_get_by_id_does_not_exist_returns_empty_list"""
        mock_template_version_manager = MagicMock()
        mock_template_version_manager_version = MagicMock()
        mock_template_version_manager.versions = [
            mock_template_version_manager_version
        ]
        mock_template_version_manager_list = [mock_template_version_manager]
        mock_get_active_global_version_manager = MagicMock()
        mock_get_active_global_version_manager.filter.return_value = (
            mock_template_version_manager_list
        )
        mock_template_version_manager_api.get_active_global_version_manager.return_value = (
            mock_get_active_global_version_manager
        )

        mock_template_api.get_by_id.side_effect = DoesNotExist(
            "mock_template_api_get_by_id_does_not_exist"
        )

        self.assertEqual(
            admin_forms._get_templates_versions(**self.mock_kwargs), []
        )

    @patch.object(admin_forms, "template_api")
    @patch.object(admin_forms, "template_version_manager_api")
    def test_successful_execution_returns_template_list(
        self, mock_template_version_manager_api, mock_template_api
    ):
        """test_successful_execution_returns_template_list"""
        mock_template_version_manager = MagicMock()
        mock_template_version_manager_version = MagicMock()
        mock_template_version_manager.versions = [
            mock_template_version_manager_version
        ]
        mock_template_version_manager_list = [mock_template_version_manager]
        mock_get_active_global_version_manager = MagicMock()
        mock_get_active_global_version_manager.filter.return_value = (
            mock_template_version_manager_list
        )
        mock_template_version_manager_api.get_active_global_version_manager.return_value = (
            mock_get_active_global_version_manager
        )

        mock_template = MagicMock()
        mock_template_api.get_by_id.return_value = mock_template

        self.assertEqual(
            admin_forms._get_templates_versions(**self.mock_kwargs),
            [
                (
                    mock_template_version_manager_version,
                    mock_template.display_name,
                )
            ],
        )


class TestGetTemplatesManager(TestCase):
    """Unit tests from `_get_templates_manager` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"request": MagicMock()}

    @patch.object(admin_forms, "template_version_manager_api")
    def test_get_active_global_version_manager_called(
        self, mock_template_version_manager_api
    ):
        """test_get_active_global_version_manager_called"""
        admin_forms._get_templates_manager(**self.mock_kwargs)

        mock_template_version_manager_api.get_active_global_version_manager.assert_called_with(
            request=self.mock_kwargs["request"]
        )

    @patch.object(admin_forms, "template_version_manager_api")
    def test_successful_execution_return_list(
        self, mock_template_version_manager_api
    ):
        """test_successful_execution_return_list"""
        mock_template_version_manager = MagicMock()
        mock_template_version_manager_list = [mock_template_version_manager]

        mock_get_active_global_version_manager = MagicMock()
        mock_get_active_global_version_manager.filter.return_value = (
            mock_template_version_manager_list
        )

        mock_template_version_manager_api.get_active_global_version_manager.return_value = (
            mock_get_active_global_version_manager
        )

        self.assertEqual(
            admin_forms._get_templates_manager(**self.mock_kwargs),
            [
                (
                    mock_template_version_manager.id,
                    mock_template_version_manager.title,
                )
            ],
        )
