""" Unit Test Rest OaiSettings
"""
from unittest.mock import patch

import requests
from django.test.testcases import SimpleTestCase
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_provider_app.rest.oai_settings import (
    views as rest_oai_settings,
)


class TestSelect(SimpleTestCase):
    """Test Select"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_select_unauthorized(self):
        """test_select_unauthorized"""

        # Arrange
        user = create_mock_user("1", is_staff=False)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_settings.Settings.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestCheckRegistry(SimpleTestCase):
    """Test Check Registry"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_check_registry_unauthorized(self):
        """test_check_registry_unauthorized"""

        # Arrange
        user = create_mock_user("1", is_staff=False)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_settings.Check.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(requests, "get")
    def test_check_registry_available(self, mock_get):
        """test_check_registry_available"""

        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_settings.Check.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(requests, "get")
    def test_check_registry_unavailable(self, mock_get):
        """test_check_registry_unavailable"""

        # Arrange
        mock_get.return_value.status_code = status.HTTP_404_NOT_FOUND
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_settings.Check.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUpdate(SimpleTestCase):
    """Test Update"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {
            "repository_name": "value",
            "repository_identifier": "value",
            "enable_harvesting": "True",
        }

    def test_update_unauthorized(self):
        """test_update_unauthorized"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_settings.Settings.as_view(),
            user=create_mock_user("1", is_staff=False),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
