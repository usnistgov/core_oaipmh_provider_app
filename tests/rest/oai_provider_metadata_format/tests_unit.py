""" Unit Test Rest OaiProviderMetadataFormat
"""
import requests
from bson.objectid import ObjectId
from django.contrib.auth.models import User
from django.test.testcases import SimpleTestCase
from mock.mock import patch, Mock
from rest_framework import status

from core_main_app.commons import exceptions
from core_main_app.components.template import api as template_api
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_provider_app.components.oai_provider_metadata_format import api as  \
    oai_provider_metadata_format_api
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import  \
    OaiProviderMetadataFormat
from core_oaipmh_provider_app.rest.oai_provider_metadata_format import views as  \
    rest_oai_provider_metadata_format


class TestSelectMetadataFormat(SimpleTestCase):
    def setUp(self):
        super(TestSelectMetadataFormat, self).setUp()
        self.data = {"metadata_format_id": str(ObjectId())}
        self.bad_data = {}

    def test_select_metadata_format_serializer_invalid(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_provider_metadata_format.select_metadata_format, user,
                           data=self.bad_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_select_metadata_format_unauthorized(self):
        # Arrange
        user = _create_mock_user(is_staff=False)

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_provider_metadata_format.select_metadata_format, user,
                           self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch.object(OaiProviderMetadataFormat, 'get_by_id')
    def test_select_metadata_format_not_found(self, mock_get_by_id):
        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_provider_metadata_format.select_metadata_format,
                           user=_create_mock_user(is_staff=True), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSelectAllMetadataFormats(SimpleTestCase):

    def setUp(self):
        super(TestSelectAllMetadataFormats, self).setUp()
        self.data = None

    def test_select_all_metadata_formats_unauthorized(self):
        # Arrange
        user = _create_mock_user(is_staff=False)

        # Act
        response = RequestMock.\
            do_request_get(rest_oai_provider_metadata_format.select_all_metadata_formats, user,
                           self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestAddMetadataFormat(SimpleTestCase):

    def setUp(self):
        super(TestAddMetadataFormat, self).setUp()
        self.data = {"metadata_prefix": "oai_test", "schema": "http://www.dummy.org"}
        self.bad_data = {}

    def test_add_metadata_format_unauthorized(self):
        # Arrange
        user = _create_mock_user(is_staff=False)

        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_metadata_format.add_metadata_format, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_metadata_format_serializer_invalid(self):
        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_metadata_format.add_metadata_format,
                            user=_create_mock_user(is_staff=True), data=self.bad_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(requests, 'get')
    def test_add_metadata_format_raises_exception_if_bad_schema_url(self, mock_get):
        # Arrange
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_404_NOT_FOUND
        mock_get.return_value.text = text

        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_metadata_format.add_metadata_format,
                            user=_create_mock_user(is_staff=True), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(requests, 'get')
    def test_add_metadata_format_raises_exception_if_bad_xml(self, mock_get):
        # Arrange
        text = '<test>Hello/test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_metadata_format.add_metadata_format,
                            user=_create_mock_user(is_staff=True), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestAddTemplateMetadataFormat(SimpleTestCase):
    def setUp(self):
        super(TestAddTemplateMetadataFormat, self).setUp()
        self.data = {"metadata_prefix": "oai_test", "template_id": str(ObjectId())}
        self.bad_data = {}

    def test_add_template_metadata_format_unauthorized(self):
        # Arrange
        user = _create_mock_user(is_staff=False)

        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_metadata_format.add_template_metadata_format, user,
                            self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_template_metadata_format_serializer_invalid(self):
        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_metadata_format.add_template_metadata_format,
                            user=_create_mock_user(is_staff=True), data=self.bad_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(template_api, 'get')
    def test_add_template_metadata_format_raises_exception_if_template_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_metadata_format.add_template_metadata_format,
                            user=_create_mock_user(is_staff=True), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUpdateMetadataFormat(SimpleTestCase):
    def setUp(self):
        super(TestUpdateMetadataFormat, self).setUp()
        self.data = {"metadata_format_id": str(ObjectId()), "metadata_prefix": "oai_update"}
        self.bad_data = {}

    def test_update_metadata_format_unauthorized(self):
        # Act
        response = RequestMock.\
            do_request_put(rest_oai_provider_metadata_format.update_metadata_format,
                           user=_create_mock_user(is_staff=False), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_metadata_format_serializer_invalid(self):
        # Act
        response = RequestMock.\
            do_request_put(rest_oai_provider_metadata_format.update_metadata_format,
                           user=_create_mock_user(is_staff=True), data=self.bad_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(OaiProviderMetadataFormat, 'get_by_id')
    def test_update_metadata_format_not_found(self, mock_get_by_id):
        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.\
            do_request_put(rest_oai_provider_metadata_format.update_metadata_format,
                           user=_create_mock_user(is_staff=True), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeleteMetadataFormat(SimpleTestCase):
    def setUp(self):
        super(TestDeleteMetadataFormat, self).setUp()
        self.data = {}
        self.bad_data = {}
        self.bad_metadata_format= {"metadata_format_id": str(ObjectId())}

    def test_delete_metadata_format_unauthorized(self):
        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_metadata_format.delete_metadata_format,
                            user=_create_mock_user(is_staff=False), data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_metadata_format_serializer_invalid(self):
        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_metadata_format.delete_metadata_format,
                            user=_create_mock_user(is_staff=True), data=self.bad_data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(oai_provider_metadata_format_api, 'get_by_id')
    def test_delete_metadata_format_not_found(self, mock_get_by_id):
        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.\
            do_request_post(rest_oai_provider_metadata_format.delete_metadata_format,
                            user=_create_mock_user(is_staff=True), data=self.bad_metadata_format)

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
