""" Int Test Rest OaiProviderSet
"""
import requests
from django.contrib.auth.models import User
from mock.mock import Mock, patch
from rest_framework import status

from core_main_app.utils.integration_tests.integration_base_test_case import \
    MongoIntegrationBaseTestCase
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_provider_app.components.oai_provider_set.models import  \
    OaiProviderSet
from core_oaipmh_provider_app.rest.oai_provider_set import views as \
    rest_oai_provider_set
from tests.utils.fixtures.fixtures import OaiPmhFixtures, OaiPmhMock


class TestSelectSet(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestSelectSet, self).setUp()
        self.data = {"set_id": str(OaiPmhMock().mock_oai_first_set().id)}

    def test_select_set_returns(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_get(rest_oai_provider_set.
                                              select_set, user=user, data=self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSelectAllSets(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestSelectAllSets, self).setUp()
        self.data = None

    def test_select_all_sets(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_get(rest_oai_provider_set.
                                              select_all_sets, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAddSet(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestAddSet, self).setUp()
        self.data = {"set_spec": "oai_dummy", "set_name": "dummy set",
                     "templates_manager": ["id1", "id2"],
                     "description": "The description"}
        self.nb_sets = len(OaiProviderSet.objects.all())

    def test_add_set(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_post(rest_oai_provider_set.add_set, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(OaiProviderSet.objects.all()), self.nb_sets + 1)


class TestDeleteSet(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestDeleteSet, self).setUp()
        self.data = {"set_id": str(OaiPmhMock().mock_oai_first_set().id)}
        self.nb_sets = len(OaiProviderSet.objects.all())

    def test_delete_set(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_post(rest_oai_provider_set.delete_set, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(OaiProviderSet.objects.all()), self.nb_sets - 1)


class TestUpdateSet(MongoIntegrationBaseTestCase):
    fixture = OaiPmhFixtures()

    def setUp(self):
        super(TestUpdateSet, self).setUp()
        self.first_set = OaiPmhMock.mock_oai_first_set()
        self.new_set_spec = "{0}_new".format(self.first_set.set_spec)
        self.new_set_name = "{0}_new".format(self.first_set.set_name)
        self.new_description = "{0}_new".format(self.first_set.description)
        self.data = {"set_id": str(self.first_set.id),
                     "set_spec": self.new_set_spec, "set_name": self.new_set_name,
                     "description": self.new_description}

    def test_update_set(self):
        # Arrange
        user = _create_mock_user(is_staff=True)

        # Act
        response = RequestMock.do_request_post(rest_oai_provider_set.update_set, user, self.data)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OaiProviderSet.objects.
                         get(pk=self.first_set.id).set_spec,
                         self.new_set_spec)
        self.assertEqual(OaiProviderSet.objects.
                         get(pk=self.first_set.id).set_name,
                         self.new_set_name)
        self.assertEqual(OaiProviderSet.objects.
                         get(pk=self.first_set.id).description,
                         self.new_description)


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
