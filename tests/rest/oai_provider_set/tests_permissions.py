""" Authentication tests for OAIProviderSet REST API
"""

from unittest.mock import patch, Mock

from django.test import SimpleTestCase
from rest_framework import status

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_provider_app.components.oai_provider_set.models import (
    OaiProviderSet,
)
from core_oaipmh_provider_app.rest.oai_provider_set import (
    views as oai_provider_views,
)
from core_oaipmh_provider_app.rest import serializers as rest_serializers


class SetListGetPermission(SimpleTestCase):
    """Set List Get Permission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_get(
            oai_provider_views.SetsList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            oai_provider_views.SetsList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiProviderSet, "get_all")
    def test_staff_returns_http_200(self, oai_provider_set_get_all):
        """test_staff_returns_http_200"""

        oai_provider_set_get_all.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            oai_provider_views.SetsList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SetListPostPermission(SimpleTestCase):
    """Set List Post Permission"""

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_post(
            oai_provider_views.SetsList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            oai_provider_views.SetsList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(
        rest_serializers.OaiProviderSetCreateUpdateSerializer, "is_valid"
    )
    @patch.object(
        rest_serializers.OaiProviderSetCreateUpdateSerializer, "save"
    )
    @patch.object(
        rest_serializers.OaiProviderSetCreateUpdateSerializer, "data"
    )
    def test_staff_returns_http_201(
        self,
        oai_provider_set_serializer_data,
        oai_provider_set_serializer_save,
        oai_provider_set_serializer_is_valid,
    ):
        """test_staff_returns_http_201"""

        oai_provider_set_serializer_data.return_value = True
        oai_provider_set_serializer_save.return_value = None
        oai_provider_set_serializer_is_valid.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            oai_provider_views.SetsList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SetDetailGetPermission(SimpleTestCase):
    """Set Detail Get Permission"""

    def setUp(self):
        """setUp"""

        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_get(
            oai_provider_views.SetDetail.as_view(),
            None,
            param={"set_id": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            oai_provider_views.SetDetail.as_view(),
            mock_user,
            param={"set_id": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiProviderSet, "get_by_id")
    @patch.object(rest_serializers.OaiProviderSetListSerializer, "data")
    def test_staff_returns_http_200(
        self, oai_provider_set_serializer_data, oai_provider_set_get_by_id
    ):
        """test_staff_returns_http_200"""

        oai_provider_set_serializer_data.return_value = True
        oai_provider_set_get_by_id.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            oai_provider_views.SetDetail.as_view(),
            mock_user,
            param={"set_id": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SetDetailDeletePermission(SimpleTestCase):
    """Set Detail Delete Permission"""

    def setUp(self):
        """setUp"""

        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_delete(
            oai_provider_views.SetDetail.as_view(),
            None,
            param={"set_id": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            oai_provider_views.SetDetail.as_view(),
            mock_user,
            param={"set_id": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiProviderSet, "get_by_id")
    @patch.object(OaiProviderSet, "delete")
    def test_staff_returns_http_204(
        self, oai_provider_set_delete, oai_provider_set_get_by_id
    ):
        """test_staff_returns_http_204"""

        oai_provider_set_get_by_id.return_value = _create_mock_provider()
        oai_provider_set_delete.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            oai_provider_views.SetDetail.as_view(),
            mock_user,
            param={"set_id": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SetDetailPatchPermission(SimpleTestCase):
    """Set Detail Patch Permission"""

    def setUp(self):
        """setUp"""

        self.fake_id = "507f1f77bcf86cd799439011"

    def test_anonymous_returns_http_403(self):
        """test_anonymous_returns_http_403"""

        response = RequestMock.do_request_patch(
            oai_provider_views.SetDetail.as_view(),
            None,
            param={"set_id": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        """test_authenticated_returns_http_403"""

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            oai_provider_views.SetDetail.as_view(),
            mock_user,
            param={"set_id": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiProviderSet, "get_by_id")
    @patch.object(
        rest_serializers.OaiProviderSetCreateUpdateSerializer, "is_valid"
    )
    @patch.object(
        rest_serializers.OaiProviderSetCreateUpdateSerializer, "save"
    )
    @patch.object(
        rest_serializers.OaiProviderSetCreateUpdateSerializer, "data"
    )
    def test_staff_returns_http_200(
        self,
        oai_provider_set_serializer_data,
        oai_provider_set_serializer_save,
        oai_provider_set_serializer_is_valid,
        oai_provider_set_get_by_id,
    ):
        """test_staff_returns_http_200"""

        oai_provider_set_get_by_id.return_value = _create_mock_provider()
        oai_provider_set_serializer_data.return_value = True
        oai_provider_set_serializer_save.return_value = None
        oai_provider_set_serializer_is_valid.return_value = {}
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            oai_provider_views.SetDetail.as_view(),
            mock_user,
            param={"set_id": self.fake_id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


def _create_mock_provider():
    """Return a mock OaiProviderSet

    Returns:

    """
    mock_provider = Mock(spec=OaiProviderSet)
    return mock_provider
