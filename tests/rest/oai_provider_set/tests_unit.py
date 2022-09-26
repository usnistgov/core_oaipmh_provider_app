""" Unit Test Rest OaiProviderSet
"""

from unittest.mock import patch
from django.test.testcases import SimpleTestCase

from rest_framework import status

from core_main_app.commons import exceptions
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_provider_app.components.oai_provider_set import (
    api as oai_provider_set_api,
)
from core_oaipmh_provider_app.components.oai_provider_set.models import (
    OaiProviderSet,
)
from core_oaipmh_provider_app.rest.oai_provider_set import (
    views as rest_oai_provider_set,
)


class TestSelectSet(SimpleTestCase):
    """Test Select Set"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"set_id": 1}
        self.bad_data = {}

    def test_select_set_unauthorized(self):
        """test_select_set_unauthorized"""

        # Arrange
        user = create_mock_user("1", is_staff=False)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_provider_set.SetDetail.as_view(), user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiProviderSet, "get_by_id")
    def test_select_set_not_found(self, mock_get_by_id):
        """test_select_set_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_get(
            rest_oai_provider_set.SetDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSelectAllSet(SimpleTestCase):
    """Test Select All Set"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_select_all_sets_unauthorized(self):
        """test_select_all_sets_unauthorized"""

        # Arrange
        user = create_mock_user("1", is_staff=False)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_provider_set.SetDetail.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAddSet(SimpleTestCase):
    """Test Add Set"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {
            "set_spec": "oai_dummy",
            "set_name": "dummy",
            "templates_manager": ["id1", "id2"],
            "description": "value",
        }
        self.bad_data = {}

    def test_add_set_unauthorized(self):
        """test_add_set_unauthorized"""

        # Arrange
        user = create_mock_user("1", is_staff=False)

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_set.SetsList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_set_serializer_invalid(self):
        """test_add_set_serializer_invalid"""

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_set.SetsList.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.bad_data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUpdateSet(SimpleTestCase):
    """Test Update Set"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"set_id": 1}
        self.data = {
            "set_spec": "oai_dummy",
            "set_name": "dummy",
            "templates_manager": ["id1", "id2"],
            "description": "value",
        }

    def test_update_set_unauthorized(self):
        """test_update_set_unauthorized"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_provider_set.SetDetail.as_view(),
            user=create_mock_user("1", is_staff=False),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiProviderSet, "get_by_id")
    def test_update_set_not_found(self, mock_get_by_id):
        """test_update_set_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_provider_set.SetDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeleteSet(SimpleTestCase):
    """Test Delete Set"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"set_id": 1}

    def test_delete_set_unauthorized(self):
        """test_delete_set_unauthorized"""

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_provider_set.SetDetail.as_view(),
            user=create_mock_user("1", is_staff=False),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(oai_provider_set_api, "get_by_id")
    def test_delete_set_not_found(self, mock_get_by_id):
        """test_delete_set_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_provider_set.SetDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
