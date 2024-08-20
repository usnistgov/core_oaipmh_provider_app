""" Unit tests for `core_oaipmh_provider_app.utils.template` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_main_app.commons.exceptions import CoreError
from core_oaipmh_provider_app.utils import template as template_utils


class TestCheckTemplateManagerInXsdFormat(TestCase):
    """Unit tests for `check_template_manager_in_xsd_format` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {
            "template_managers_id_list": MagicMock(),
            "request": MagicMock(),
        }

    @patch.object(template_utils, "template_version_manager_api")
    def test_get_by_id_list_called(self, mock_template_version_manager_api):
        """test_get_by_id_list_called"""
        with self.assertRaises(CoreError):
            template_utils.check_template_manager_in_xsd_format(
                **self.mock_kwargs
            )

        mock_template_version_manager_api.get_by_id_list.assert_called_with(
            self.mock_kwargs["template_managers_id_list"],
            self.mock_kwargs["request"],
        )

    @patch.object(template_utils, "template_version_manager_api")
    def test_not_all_xsd_templates_raises_validation_error(
        self, mock_template_version_manager_api
    ):
        """test_not_all_xsd_templates_raises_validation_error"""
        mock_template_version_manager_list = MagicMock()

        mock_template_version_manager_list.count.return_value = 2

        mock_filter = MagicMock()
        mock_filter.count.return_value = 1
        mock_template_version_manager_list.filter.return_value = mock_filter

        mock_template_version_manager_api.get_by_id_list.return_value = (
            mock_template_version_manager_list
        )

        with self.assertRaises(CoreError):
            template_utils.check_template_manager_in_xsd_format(
                **self.mock_kwargs
            )

    @patch.object(template_utils, "template_version_manager_api")
    def test_all_xsd_templates_returns_none(
        self, mock_template_version_manager_api
    ):
        """test_all_xsd_templates_returns_none"""
        mock_template_version_manager_list = MagicMock()

        mock_template_version_manager_list.count.return_value = 1

        mock_filter = MagicMock()
        mock_filter.count.return_value = 1
        mock_template_version_manager_list.filter.return_value = mock_filter

        mock_template_version_manager_api.get_by_id_list.return_value = (
            mock_template_version_manager_list
        )

        self.assertIsNone(
            template_utils.check_template_manager_in_xsd_format(
                **self.mock_kwargs
            )
        )
