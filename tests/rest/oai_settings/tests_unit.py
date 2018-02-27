""" Unit Test Rest OaiSettings
"""
import requests
from django.contrib.auth.models import User
from django.test.testcases import SimpleTestCase
from mock.mock import Mock, patch
from rest_framework import status

from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_provider_app.rest.oai_settings import views as  \
    rest_oai_settings


class TestSelect(SimpleTestCase):
    def setUp(self):
        super(TestSelect, self).setUp()
        self.data = None

    def test_select_unauthorized(self):
        # Arrange
        user = _create_mock_user(is_staff=False)

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_settings.Settings.as_view(), user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCheckRegistry(SimpleTestCase):
    def setUp(self):
        super(TestCheckRegistry, self).setUp()
        self.data = None

    def test_check_registry_unauthorized(self):
        # Arrange
        user = _create_mock_user(is_staff=False)

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_settings.Check.as_view(), user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch.object(requests, 'get')
    def test_check_registry_available(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = status.HTTP_200_OK
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_settings.Check.as_view(), user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(requests, 'get')
    def test_check_registry_unavailable(self, mock_get):
        # Arrange
        mock_get.return_value.status_code = status.HTTP_404_NOT_FOUND
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock. \
            do_request_get(rest_oai_settings.Check.as_view(), user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUpdate(SimpleTestCase):
    def setUp(self):
        super(TestUpdate, self).setUp()
        self.data = {"repository_name": "value", "repository_identifier": "value",
                     "enable_harvesting": "True"}

    def test_update_unauthorized(self):
        # Act
        response = RequestMock.\
            do_request_patch(rest_oai_settings.Settings.as_view(),
                             user=_create_mock_user(is_staff=False), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


def _create_mock_user(is_staff=False, has_perm=False, is_anonymous=False):
    """ Mock an User.

        Returns:
            User mock.

    """
    mock_user = Mock(spec=User)
    mock_user.is_staff = is_staff
    if is_staff:
        mock_user.has_perm.return_value = True
        mock_user.is_anonymous.return_value = False
    else:
        mock_user.has_perm.return_value = has_perm
        mock_user.is_anonymous.return_value = is_anonymous

    return mock_user
