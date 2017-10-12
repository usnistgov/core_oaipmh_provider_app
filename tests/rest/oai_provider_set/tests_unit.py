""" Unit Test Rest OaiProviderSet
"""
from bson.objectid import ObjectId
from django.contrib.auth.models import User
from django.test.testcases import SimpleTestCase
from mock.mock import patch, Mock
from rest_framework import status

from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_provider_app.components.oai_provider_set import api as  \
    oai_provider_set_api
from core_oaipmh_provider_app.components.oai_provider_set.models import  \
    OaiProviderSet
from core_oaipmh_provider_app.rest.oai_provider_set import views as  \
    rest_oai_provider_set


class TestSelectSet(SimpleTestCase):
    def setUp(self):
        super(TestSelectSet, self).setUp()
        self.data = {"set_id": str(ObjectId())}
        self.bad_data = {}

    def test_select_set_serializer_invalid(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_provider_set.select_set, user,
                           data=self.bad_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_select_set_unauthorized(self):
        # Arrange
        user = _create_mock_user(is_staff=False)

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_provider_set.select_set, user,
                           self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch.object(OaiProviderSet, 'get_by_id')
    def test_select_set_not_found(self, mock_get_by_id):
        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_provider_set.select_set,
                           user=_create_mock_user(is_staff=True), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSelectAllSet(SimpleTestCase):

    def setUp(self):
        super(TestSelectAllSet, self).setUp()
        self.data = None

    def test_select_all_sets_unauthorized(self):
        # Arrange
        user = _create_mock_user(is_staff=False)

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_provider_set.select_all_sets, user,
                           self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAddSet(SimpleTestCase):

    def setUp(self):
        super(TestAddSet, self).setUp()
        self.data = {"set_spec": "oai_dummy", "set_name": "dummy",
                     "templates_manager": ["id1", "id2"], "description": "value"}
        self.bad_data = {}

    def test_add_set_unauthorized(self):
        # Arrange
        user = _create_mock_user(is_staff=False)

        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_set.add_set, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_set_serializer_invalid(self):
        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_set.add_set,
                            user=_create_mock_user(is_staff=True), data=self.bad_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUpdateSet(SimpleTestCase):
    def setUp(self):
        super(TestUpdateSet, self).setUp()
        self.data = {"set_id": str(ObjectId()), "set_spec": "oai_dummy", "set_name": "dummy",
                     "templates_manager": ["id1", "id2"], "description": "value"}
        self.bad_data = {}

    def test_update_set_unauthorized(self):
        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_set.update_set,
                            user=_create_mock_user(is_staff=False), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_set_serializer_invalid(self):
        # Act
        response = RequestMock. \
            do_request_post(rest_oai_provider_set.update_set,
                            user=_create_mock_user(is_staff=True), data=self.bad_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(OaiProviderSet, 'get_by_id')
    def test_update_set_not_found(self, mock_get_by_id):
        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock. \
            do_request_post(rest_oai_provider_set.update_set,
                            user=_create_mock_user(is_staff=True), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeleteSet(SimpleTestCase):
    def setUp(self):
        super(TestDeleteSet, self).setUp()
        self.data = {}
        self.bad_data = {}
        self.bad_set = {"set_id": str(ObjectId())}

    def test_delete_set_unauthorized(self):
        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_set.delete_set,
                            user=_create_mock_user(is_staff=False), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_set_serializer_invalid(self):
        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_set.delete_set,
                            user=_create_mock_user(is_staff=True), data=self.bad_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(oai_provider_set_api, 'get_by_id')
    def test_delete_set_not_found(self, mock_get_by_id):
        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_set.delete_set,
                            user=_create_mock_user(is_staff=True), data=self.bad_set)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
