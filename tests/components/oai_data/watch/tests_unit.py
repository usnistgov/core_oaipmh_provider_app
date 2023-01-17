""" Unit tests for OaiData signals
"""
from unittest.case import TestCase
from unittest.mock import patch, Mock

from core_main_app.commons.exceptions import DoesNotExist
from core_oaipmh_provider_app.components.oai_data.watch import pre_delete_data


class TestPreDeleteData(TestCase):
    """Tests for pre_delete_data function"""

    @patch("core_oaipmh_provider_app.components.oai_data.api.get_by_data")
    @patch("core_oaipmh_provider_app.components.oai_data.api.upsert")
    def test_no_upsert_if_oai_data_does_not_exist(
        self, mock_upsert, mock_get_by_data
    ):
        mock_get_by_data.side_effect = DoesNotExist("mock_does_not_exist")

        pre_delete_data(Mock(), Mock())

        self.assertFalse(mock_upsert.called)

    @patch("core_oaipmh_provider_app.components.oai_data.api.get_by_data")
    @patch("core_oaipmh_provider_app.components.oai_data.api.upsert")
    def test_upsert_if_oai_data_exists(self, mock_upsert, mock_get_by_data):
        mock_get_by_data.return_value = Mock()

        pre_delete_data(Mock(), Mock())

        self.assertTrue(mock_upsert.called)
