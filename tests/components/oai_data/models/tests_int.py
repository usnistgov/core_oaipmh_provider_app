""" Integration testing of OaiData model
"""
from core_main_app.system import api as system_api
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_oaipmh_provider_app.components.oai_data.models import OaiData
from tests.utils.fixtures.fixtures import OaiPmhFixtures


class TestOaiDataGetAllByTemplateListAndTimeframe(IntegrationBaseTestCase):
    """Test OaiData get_all_by_template_list_and_timeframe method"""

    fixture = OaiPmhFixtures()

    def test_correct_items_returned(self):
        """test_correct_items_returned"""
        template = system_api.get_template_by_id(1)
        results = OaiData.get_all_by_template_list_and_timeframe(
            [template], None, None
        )

        self.assertEqual(list(results), list(OaiData.objects.all()))


class TestOaiDataGetAllByTemplateAndTimeframe(IntegrationBaseTestCase):
    """Test OaiData get_all_by_template_and_timeframe method"""

    fixture = OaiPmhFixtures()

    def test_correct_items_returned(self):
        """test_correct_items_returned"""
        template = system_api.get_template_by_id(1)
        results = OaiData.get_all_by_template_and_timeframe(
            template, None, None
        )

        self.assertEqual(list(results), list(OaiData.objects.all()))
