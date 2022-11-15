"""Test Apps file
"""

from unittest.case import TestCase

from core_main_app.commons.exceptions import CoreError
from core_oaipmh_provider_app.apps import _check_settings


class TestCheckSettings(TestCase):
    """Test Check Settings"""

    def test_check_settings_with_expected_settings_works(self):
        """test_check_settings_with_expected_settings_works"""

        _check_settings(
            can_set_public_data_to_private=False,
            can_set_workspace_public=False,
            can_anonymous_access_public_document=True,
        )

    def test_check_settings_one_incorrect_settings_raises_error(self):
        """test_check_settings_one_incorrect_settings_raises_error

        Returns:

        """
        with self.assertRaises(CoreError):
            _check_settings(
                can_set_public_data_to_private=True,
                can_set_workspace_public=False,
                can_anonymous_access_public_document=True,
            )

    def test_check_settings_two_incorrect_settings_raises_error(self):
        """test_check_settings_two_incorrect_settings_raises_error

        Returns:

        """
        with self.assertRaises(CoreError):
            _check_settings(
                can_set_public_data_to_private=True,
                can_set_workspace_public=True,
                can_anonymous_access_public_document=True,
            )

    def test_check_settings_all_incorrect_settings_raises_error(self):
        """test_check_settings_all_incorrect_settings_raises_error

        Returns:

        """
        with self.assertRaises(CoreError):
            _check_settings(
                can_set_public_data_to_private=True,
                can_set_workspace_public=True,
                can_anonymous_access_public_document=False,
            )
