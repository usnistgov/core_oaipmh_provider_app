""" Unit tests for OaiData model.
"""

import operator
from unittest import TestCase
from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist

from core_main_app.commons.exceptions import DoesNotExist, ModelError
from core_oaipmh_provider_app.components.oai_data.models import OaiData
from tests.components.oai_data import _create_oai_data
from tests.utils.mocks import MockPassThrough


class TestOaiDataFilterByDate(TestCase):
    """Test OaiData _filter_by_date method"""

    def test_param_none_returns_empty_list(self):
        """test_param_none_returns_empty_list"""
        self.assertEqual(OaiData._filter_by_date(None, None), [])

    @patch("core_oaipmh_provider_app.components.oai_data.models.Q")
    def test_from_param_returns_correct_list(self, mock_q):
        """test_from_param_returns_correct_list"""
        mock_q.side_effect = MockPassThrough
        mock_from = "mock_from"

        results = OaiData._filter_by_date(mock_from, None)

        self.assertEqual(len(results), 1)
        self.assertDictEqual(
            results[0].kwargs, {"oai_date_stamp__gte": "mock_from"}
        )

    @patch("core_oaipmh_provider_app.components.oai_data.models.Q")
    def test_until_param_returns_correct_list(self, mock_q):
        """test_until_param_returns_correct_list"""
        mock_q.side_effect = MockPassThrough
        mock_until = "mock_until"

        results = OaiData._filter_by_date(None, mock_until)

        self.assertEqual(len(results), 1)
        self.assertDictEqual(
            results[0].kwargs, {"oai_date_stamp__lte": mock_until}
        )

    @patch("core_oaipmh_provider_app.components.oai_data.models.Q")
    def test_from_and_until_param_returns_correct_list(self, mock_q):
        """test_from_and_until_param_returns_correct_list"""
        mock_q.side_effect = MockPassThrough
        mock_from = "mock_from"
        mock_until = "mock_until"

        results = OaiData._filter_by_date(mock_from, mock_until)

        self.assertEqual(len(results), 2)
        self.assertDictEqual(
            results[0].kwargs, {"oai_date_stamp__gte": mock_from}
        )
        self.assertDictEqual(
            results[1].kwargs, {"oai_date_stamp__lte": mock_until}
        )


class TestOaiDataFilterPublicData(TestCase):
    """Test OaiData _filter_public_data method"""

    @patch("core_oaipmh_provider_app.components.oai_data.models.Q")
    def test_returns_correct_list(self, mock_q):
        """test_returns_correct_list"""
        mock_q.side_effect = MockPassThrough

        results = OaiData._filter_public_data()

        self.assertEqual(len(results), 2)
        self.assertDictEqual(
            results[0].kwargs, {"data__workspace__isnull": False}
        )
        self.assertDictEqual(
            results[1].kwargs, {"data__workspace__is_public": True}
        )


class TestOaiDataGetByData(TestCase):
    """Test OaiData get_by_data method"""

    @patch(
        "core_oaipmh_provider_app.components.oai_data.models.OaiData.objects.get"
    )
    def test_returns_oai_data_object(self, mock_oai_get):
        """test_returns_oai_data_object"""
        mock_oai_data = "mock_oai_data"
        mock_oai_get.return_value = mock_oai_data

        self.assertEqual(OaiData.get_by_data("mock_data"), mock_oai_data)

    @patch(
        "core_oaipmh_provider_app.components.oai_data.models.OaiData.objects.get"
    )
    def test_does_not_exists_raises_does_not_exist(self, mock_oai_get):
        """test_does_not_exists_raises_does_not_exist"""
        mock_oai_get.side_effect = ObjectDoesNotExist(
            "mock_object_does_not_exist"
        )

        with self.assertRaises(DoesNotExist):
            OaiData.get_by_data("mock_data")

    @patch(
        "core_oaipmh_provider_app.components.oai_data.models.OaiData.objects.get"
    )
    def test_any_error_raises_model_error(self, mock_oai_get):
        """test_any_error_raises_model_error"""
        mock_oai_get.side_effect = Exception("mock_exception")

        with self.assertRaises(ModelError):
            OaiData.get_by_data("mock_data")


class TestOaiDataGetAll(TestCase):
    """Test OaiData get_all method"""

    @patch(
        "core_oaipmh_provider_app.components.oai_data.models.OaiData.objects.all"
    )
    def test_returns_all_oai_data(self, mock_oai_all):
        """test_returns_all_oai_data"""
        mock_all_oai_data = ["mock_oai_data"]
        mock_oai_all.return_value = mock_all_oai_data

        self.assertEqual(OaiData.get_all(), mock_all_oai_data)


class TestOaiDataGetAllByDataListAndTimeframe(TestCase):
    """Test OaiData get_all_by_data_list_and_timeframe method"""

    @patch("core_oaipmh_provider_app.components.oai_data.models.reduce")
    @patch(
        "core_oaipmh_provider_app.components.oai_data.models.OaiData.objects.filter"
    )
    @patch(
        "core_oaipmh_provider_app.components.oai_data.models.OaiData._filter_by_date"
    )
    @patch("core_oaipmh_provider_app.components.oai_data.models.Q")
    def test_return_correct_filter(
        self,
        mock_q,
        mock_filter_by_date,
        mock_objects_filter,
        mock_reduce,
    ):
        """test_return_correct_filter"""
        mock_q.side_effect = MockPassThrough
        mock_filter_by_date.return_value = ["mock_filter_by_date"]
        mock_objects_filter.side_effect = MockPassThrough
        mock_reduce.side_effect = MockPassThrough

        results = OaiData.get_all_by_data_list_and_timeframe(
            "mock_data_list", "mock_from", "mock_until"
        )
        self.assertEqual(len(results.args[0].args), 2)
        self.assertEqual(results.args[0].args[0], operator.and_)

        results_qlist = results.args[0].args[1]
        self.assertEqual(len(results_qlist), 2)
        self.assertEqual(
            results_qlist[0].kwargs, {"data__in": "mock_data_list"}
        )
        self.assertEqual(results_qlist[1], "mock_filter_by_date")


class TestOaiDataGetAllByTemplateAndTimeframe(TestCase):
    """Test OaiData get_all_by_template_and_timeframe method"""

    @patch("core_oaipmh_provider_app.components.oai_data.models.reduce")
    @patch(
        "core_oaipmh_provider_app.components.oai_data.models.OaiData.objects.filter"
    )
    @patch(
        "core_oaipmh_provider_app.components.oai_data.models.OaiData._filter_by_date"
    )
    @patch("core_oaipmh_provider_app.components.oai_data.models.Q")
    def test_return_correct_filter(
        self,
        mock_q,
        mock_filter_by_date,
        mock_objects_filter,
        mock_reduce,
    ):
        """test_return_correct_filter"""
        mock_q.side_effect = MockPassThrough
        mock_filter_by_date.return_value = ["mock_filter_by_date"]
        mock_objects_filter.side_effect = MockPassThrough
        mock_reduce.side_effect = MockPassThrough

        results = OaiData.get_all_by_template_and_timeframe(
            "mock_template", "mock_from", "mock_until"
        )
        self.assertEqual(len(results.args[0].args), 2)
        self.assertEqual(results.args[0].args[0], operator.and_)

        results_qlist = results.args[0].args[1]
        self.assertEqual(len(results_qlist), 2)
        self.assertEqual(
            results_qlist[0].kwargs, {"template": "mock_template"}
        )
        self.assertEqual(results_qlist[1], "mock_filter_by_date")


class TestOaiDataStr(TestCase):
    """TestOaiDataStr"""

    def test_oai_data_str_uses_data_title_if_not_None(self):
        """oai_data_str_uses_data_title_if_not_None

        Returns:

        """
        oai_data = _create_oai_data()
        oai_data.data.title = "test"
        self.assertTrue("test" in oai_data.__str__())

    def test_oai_data_str_uses_deleted_label_if_data_is_None(self):
        """oai_data_str_uses_deleted_label_if_data_is_None

        Returns:

        """
        oai_data = _create_oai_data()
        oai_data.data = None
        self.assertTrue("DELETED" in oai_data.__str__())
