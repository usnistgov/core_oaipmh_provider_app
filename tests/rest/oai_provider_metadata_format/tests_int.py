""" Int Test Rest OaiProviderMetadataFormat
"""
import requests
from django.contrib.auth.models import User
from mock.mock import Mock, patch
from rest_framework import status

from core_main_app.utils.integration_tests.integration_base_test_case import MongoIntegrationBaseTestCase
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import  \
    OaiProviderMetadataFormat
from core_oaipmh_provider_app.rest.oai_provider_metadata_format import views as \
    rest_oai_provider_metadata_format
from tests.utils.fixtures.fixtures import OaiPmhFixtures, OaiPmhMock


class TestSelectMetadataFormat(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestSelectMetadataFormat, self).setUp()
        self.data = {"metadata_format_id": str(OaiPmhMock().mock_oai_first_metadata_format().id)}

    def test_select_metadata_format_returns(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_get(rest_oai_provider_metadata_format.
                                              select_metadata_format, user=user, data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSelectAllMetadataFormats(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestSelectAllMetadataFormats, self).setUp()
        self.data = None

    def test_select_all_metadata_formats(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_get(rest_oai_provider_metadata_format.
                                              select_all_metadata_formats, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAddMetadataFormat(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestAddMetadataFormat, self).setUp()
        self.data = {"metadata_prefix": "oai_test", "schema": "http://www.dummy.org"}
        self.nb_metadata_formats = len(OaiProviderMetadataFormat.objects.all())

    @patch.object(requests, 'get')
    def test_add_metadata_format(self, mock_get):
        # Arrange
        text = '<test>Hello</test>'
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_post(rest_oai_provider_metadata_format.
                                               add_metadata_format, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(OaiProviderMetadataFormat.objects.all()), self.nb_metadata_formats + 1)


class TestAddTemplateMetadataFormat(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestAddTemplateMetadataFormat, self).setUp()
        self.data = {"metadata_prefix": "oai_test", "template_id": str(
            OaiPmhMock.mock_oai_first_template().id)}
        self.nb_template_metadata_formats = len(OaiProviderMetadataFormat.objects.all())

    def test_add_template_metadata_format(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_post(rest_oai_provider_metadata_format.
                                               add_template_metadata_format, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(OaiProviderMetadataFormat.objects.all()),
                         self.nb_template_metadata_formats + 1)


class TestDeleteMetadataFormat(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestDeleteMetadataFormat, self).setUp()
        self.data = {"metadata_format_id": str(OaiPmhMock().mock_oai_first_metadata_format().id)}
        self.nb_metadata_formats = len(OaiProviderMetadataFormat.objects.all())

    def test_delete_metadata_format(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_post(rest_oai_provider_metadata_format.
                                               delete_metadata_format, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(OaiProviderMetadataFormat.objects.all()), self.nb_metadata_formats - 1)


class TestUpdateMetadataFormat(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestUpdateMetadataFormat, self).setUp()
        self.first_metadata_format = OaiPmhMock.mock_oai_first_metadata_format()
        self.new_metadata_prefix = "{0}_new".format(self.first_metadata_format.metadata_prefix)
        self.data = {"metadata_format_id": str(self.first_metadata_format.id),
                     "metadata_prefix": self.new_metadata_prefix}

    def test_update_metadata_format(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_put(rest_oai_provider_metadata_format.
                                              update_metadata_format, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OaiProviderMetadataFormat.objects.
                         get(pk=self.first_metadata_format.id).metadata_prefix,
                         self.new_metadata_prefix)


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
