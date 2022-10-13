""" Int Test Rest OaiProviderSet
"""

from rest_framework import status


from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_provider_app.components.oai_provider_set.models import (
    OaiProviderSet,
)
from core_oaipmh_provider_app.rest.oai_provider_set import (
    views as rest_oai_provider_set,
)
from tests.utils.fixtures.fixtures import OaiPmhFixtures, OaiPmhMock


class TestSelectSet(MongoIntegrationBaseTestCase):
    """Test Select Set"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"set_id": str(OaiPmhMock().mock_oai_first_set().id)}

    def test_select_set_returns(self):
        """test_select_set_returns"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_provider_set.SetDetail.as_view(),
            user=user,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestSelectAllSets(MongoIntegrationBaseTestCase):
    """Test Select All Sets"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_select_all_sets(self):
        """test_select_all_sets"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_provider_set.SetsList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAddSet(MongoIntegrationBaseTestCase):
    """Test Add Set"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {
            "set_spec": "oai_dummy",
            "set_name": "dummy set",
            "templates_manager": [],
            "description": "The description",
        }
        self.nb_sets = len(OaiProviderSet.objects.all())

    def test_add_set(self):
        """test_add_set"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_set.SetsList.as_view(), user, self.data
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(OaiProviderSet.objects.all()), self.nb_sets + 1)


class TestDeleteSet(MongoIntegrationBaseTestCase):
    """Test Delete Set"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"set_id": str(OaiPmhMock().mock_oai_first_set().id)}
        self.nb_sets = len(OaiProviderSet.objects.all())

    def test_delete_set(self):
        """test_delete_set"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_provider_set.SetDetail.as_view(), user, param=self.param
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(OaiProviderSet.objects.all()), self.nb_sets - 1)


class TestUpdateSet(MongoIntegrationBaseTestCase):
    """Test Update Set"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""

        super().setUp()
        self.first_set = OaiPmhMock.mock_oai_first_set()
        self.new_set_spec = "{0}_new".format(self.first_set.set_spec)
        self.new_set_name = "{0}_new".format(self.first_set.set_name)
        self.new_description = "{0}_new".format(self.first_set.description)
        self.new_template_version = self.fixture.template_version_managers[0]
        self.param = {"set_id": str(self.first_set.id)}
        self.data = {
            "set_spec": self.new_set_spec,
            "set_name": self.new_set_name,
            "description": self.new_description,
            "templates_manager": [self.new_template_version.pk],
        }

    def test_update_set(self):
        """test_update_set"""

        # Arrange
        user = create_mock_user("1", is_staff=True)

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_provider_set.SetDetail.as_view(),
            user,
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            OaiProviderSet.objects.get(pk=self.first_set.id).set_spec,
            self.new_set_spec,
        )
        self.assertEqual(
            OaiProviderSet.objects.get(pk=self.first_set.id).set_name,
            self.new_set_name,
        )
        self.assertEqual(
            OaiProviderSet.objects.get(pk=self.first_set.id).description,
            self.new_description,
        )
        self.assertEqual(
            list(
                OaiProviderSet.objects.get(
                    pk=self.first_set.id
                ).templates_manager.all()
            ),
            [self.new_template_version],
        )
