""" Integrations testing of the OaiData API
"""

from django.db.models import Q

from core_main_app.components.data.models import Data
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_oaipmh_provider_app.components.oai_data import api as oai_data_api
from tests.utils.fixtures.fixtures import OaiPmhFixtures, OaiPmhMock


class TestUpsertFromData(IntegrationBaseTestCase):
    """Test upsert_from_data API call"""

    fixture = OaiPmhFixtures()

    def setUp(self):
        """setUp"""
        super().setUp()

        self.template = OaiPmhMock.mock_template()[0]
        self.workspace = OaiPmhMock.mock_workspaces()[0]

    def _upsert_oai_data_and_assert(self, data):
        """_upsert_oai_data_and_assert"""
        oai_data_api.upsert_from_data(data)
        all_oai_data = [oai_data.data for oai_data in oai_data_api.get_all()]

        self.assertIn(None, all_oai_data)
        self.assertEqual(
            [data for data in all_oai_data if data],
            list(
                Data.objects.filter(
                    Q(
                        workspace__in=[self.workspace.pk],
                        template__in=[self.template.pk],
                    )
                )
            ),
        )

    def test_archived_data_does_not_create_oai_data(self):
        """test_archived_data_does_not_create_oai_data"""
        archived_data = OaiPmhMock.mock_data()[0]
        oai_data_api.upsert_from_data(archived_data)

        self._upsert_oai_data_and_assert(archived_data)

    def test_private_data_does_not_create_oai_data(self):
        """test_private_data_does_not_create_oai_data"""
        private_data = OaiPmhMock.mock_data()[1]
        # Ensure the data is not in any workspace
        assert private_data.workspace is None

        self._upsert_oai_data_and_assert(private_data)

    def test_new_data_create_oai_data(self):
        """test_new_data_create_oai_data"""
        new_data = OaiPmhMock.mock_data()[0]
        new_data.pk = len(self.fixture.data) + 1
        new_data.title = f"Test {new_data.pk}"
        new_data.template = self.template
        new_data.workspace = self.workspace
        new_data.save()

        self._upsert_oai_data_and_assert(new_data)
